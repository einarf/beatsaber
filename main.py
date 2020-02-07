import copy
import json
import math

import moderngl
import moderngl_window
from pyrr import Matrix44
from pyglet.media import Player, StaticSource, load
from moderngl_window.scene import KeyboardCamera, MeshProgram
from moderngl_window import geometry
from track import BSTrack, EventType


class BeatSaberMap:

    def __init__(self, scene, track):
        self.scene = scene
        self.track = track

        # Objects & Materials
        self.mat_back_lights = self.scene.find_material(name="Back Lights")
        # Light rails on left and right side (ROAD_LIGHTS)
        self.road_lights_material = self.scene.find_material(name="Center Lights")
        self.right_lasers_material = self.scene.find_material(name="Right Lasers")
        self.left_lasers_material = self.scene.find_material(name="Left Lasers")
        self.back_lasers_material = self.scene.find_material(name="Back Lights")
        self.ring_lights_material = copy.deepcopy(self.scene.find_material(name="Ring Neons.004"))
        # Hack in the same material for each neon ring for now
        for ring in range(21, 32):
            ring_name = "Ring.{}".format(str(ring).zfill(3))
            self.scene.find_node(ring_name).children[0].mesh.material = self.ring_lights_material
            self.scene.find_node(ring_name).children[2].mesh.material = self.ring_lights_material
            self.scene.find_node(ring_name).children[3].mesh.material = self.ring_lights_material
            self.scene.find_node(ring_name).children[4].mesh.material = self.ring_lights_material

        # Static unlit par of the map
        self.highway = self.scene.find_node(name="Highway")
        self.highway.mesh.material.color = 0.1, 0.1, 0.1, 0.05
        unlit_material = self.highway.mesh.material
        for ring in range(21, 32):
            ring_name = "Ring.{}".format(str(ring).zfill(3))
            self.scene.find_node(ring_name).children[1].mesh.material = unlit_material

        self.light_center = self.scene.find_node(name="Center Lights")

        # Rings
        self.ring_01 = self.scene.find_node(name='Ring.001')
        self.ring_02 = self.scene.find_node(name='Ring.001')

        # Left laser
        self.laser_left_01 = self.scene.find_node(name="Left 1")
        self.laser_left_02 = self.scene.find_node(name="Left 2")
        self.laser_left_03 = self.scene.find_node(name="Left 3")
        self.laser_left_04 = self.scene.find_node(name="Left 4")

        # Right laser
        self.laser_right_01 = self.scene.find_node(name="Right 1")
        self.laser_right_02 = self.scene.find_node(name="Right 2")
        self.laser_right_03 = self.scene.find_node(name="Right 3")
        self.laser_right_04 = self.scene.find_node(name="Right 4")

        # Ring Neons
        self.neon_1 = self.scene.find_material(name="Ring Neons.022")
        self.neon_2 = self.scene.find_material(name="Ring Neons.021")
        self.neon_3 = self.scene.find_material(name="Ring Neons.020")
        self.neon_4 = self.scene.find_material(name="Ring Neons.027")

    def render(self, camera, time, frame_time):
        self.process_events(time)
        self.scene.draw(camera.projection.matrix, camera.matrix)

    def process_events(self, time):
        ms_time = int(time * 1000)
        color, t = self.track.get_value(EventType.ROAD_LIGHTS, ms_time)
        self.road_lights_material.color = color
        color, t = self.track.get_value(EventType.RIGHT_LASERS, ms_time)
        self.right_lasers_material.color = color
        color, t = self.track.get_value(EventType.LEFT_LASERS, ms_time)
        self.left_lasers_material.color = color
        color, t = self.track.get_value(EventType.BACK_LASERS, ms_time)
        self.back_lasers_material.color = color
        color, t = self.track.get_value(EventType.RING_LIGHTS, ms_time)
        self.ring_lights_material.color = color

        self.laser_left_01
        # 0 1 3 5 10 20


class LaserProgram(MeshProgram):
    pass


class BeatSaber(moderngl_window.WindowConfig):
    title = "Beat Saber Light Show"
    resource_dir = './resources'
    window_size = 1920, 1080

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = False
        self.bpm = 242  # Hardcode bpm from info.dat
        self.camera = KeyboardCamera(self.wnd.keys, near=1.0, far=1000.0)
        self.camera.velocity = 50
        self.camera_enabled = False

        with open('./resources/megalovania_remix/info.dat') as fd:
            meta = json.load(fd)

        self.map = BeatSaberMap(
            self.load_scene('bs_map.glb'),
            BSTrack('./resources/megalovania_remix/Expert.dat', meta['_beatsPerMinute']),
        )

        self.quad_fs = geometry.quad_fs()
        # blur stuff
        self.offscreen_texture = self.ctx.texture((self.wnd.buffer_width, self.wnd.buffer_height), 4)
        self.offscreen_depth = self.ctx.depth_texture((self.wnd.buffer_width, self.wnd.buffer_height))
        self.offscreen = self.ctx.framebuffer(
            color_attachments=[self.offscreen_texture],
            depth_attachment=self.offscreen_depth,
        )
        bd = 16
        self.blur_h_texture = self.ctx.texture((self.wnd.buffer_width // bd, self.wnd.buffer_height // bd), 4)
        self.blur_h = self.ctx.framebuffer(color_attachments=[self.blur_h_texture])
        self.blur_v_texture = self.ctx.texture((self.wnd.buffer_width // bd, self.wnd.buffer_height // bd), 4)
        self.blur_v = self.ctx.framebuffer(color_attachments=[self.blur_v_texture])

        self.copy_prog = self.load_program('programs/copy.glsl')
        self.copy_greyscale_prog = self.load_program('programs/copy_greyscale.glsl')
        self.blur_h_prog = self.load_program('programs/blur_h.glsl')
        self.blur_v_prog = self.load_program('programs/blur_v.glsl')

        self.music_player = Player()
        self.music_source = StaticSource(load('./resources/megalovania_remix/song.wav'))
        self.music_player.queue(self.music_source)
        self.music_player.play()
        self.music_player.seek(60.0 * 5)
        self.music_player.volume = 0.001

    def render(self, time, frame_time):
        # self.offscreen.clear()
        # self.blur_h.clear()
        # self.blur_v.clear()
        time = self.music_player.time

        # self.offscreen.use()
        self.ctx.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.map.render(self.camera, time, frame_time)

        # self.ctx.enable_only(moderngl.NOTHING)

        # self.blur_v.use()
        # self.offscreen_texture.use(location=0)
        # self.quad_fs.render(self.copy_prog)

        # self.blur_h.use()
        # self.blur_v_texture.use(location=0)
        # self.quad_fs.render(self.blur_h_prog)

        # self.blur_v.use()
        # self.blur_h_texture.use(location=0)
        # self.quad_fs.render(self.blur_v_prog)

        # # Back to screen
        # self.wnd.fbo.use()
        # self.offscreen_texture.use()
        # self.quad_fs.render(self.copy_greyscale_prog)
        # self.ctx.enable_only(moderngl.BLEND)
        # self.ctx.blend_func = moderngl.ONE, moderngl.ONE
        # self.blur_v_texture.use(location=0)
        # self.quad_fs.render(self.copy_prog)

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if self.camera_enabled:
            self.camera.key_input(key, action, modifiers)

        if action == keys.ACTION_PRESS:
            if key == keys.C:
                self.camera_enabled = not self.camera_enabled
                self.wnd.mouse_exclusivity = self.camera_enabled
                self.wnd.cursor = not self.camera_enabled
            if key == keys.SPACE:
                self.timer.toggle_pause()

    def mouse_position_event(self, x: int, y: int, dx, dy):
        if self.camera_enabled:
            self.camera.rot_state(-dx, -dy)

    def resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)


if __name__ == '__main__':
    moderngl_window.run_window_config(BeatSaber)
