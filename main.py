import copy
import math

import moderngl
import moderngl_window
from pyrr import Matrix44
from pyglet.media import Player, StaticSource, load
from moderngl_window.scene.camera import KeyboardCamera
from track import BSTrack, EventType


class BeatSaberMap:

    def __init__(self, scene, track):
        self.scene = scene
        self.track = track

        # Objects & Materials
        self.mat_back_lights = self.scene.find_material(name="Back Lights")
        # Light rails on left and right side (ROAD_LIGHTS)
        self.road_lights = self.scene.find_material(name="Center Lights")
        self.right_lasers = self.scene.find_material(name="Right Lasers")
        self.left_lasers = self.scene.find_material(name="Left Lasers")
        self.back_lasers = self.scene.find_material(name="Back Lights")
        self.ring_lights = copy.deepcopy(self.scene.find_material(name="Ring Neons.004"))
        # Hack in the same material for each neon ring for now
        for ring in range(21, 32):
            ring_name = "Ring.{}".format(str(ring).zfill(3))
            self.scene.find_node(ring_name).children[0].mesh.material = self.ring_lights
            self.scene.find_node(ring_name).children[2].mesh.material = self.ring_lights
            self.scene.find_node(ring_name).children[3].mesh.material = self.ring_lights
            self.scene.find_node(ring_name).children[4].mesh.material = self.ring_lights

        # Static unlit par of the map
        self.highway = self.scene.find_node(name="Highway")

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
        self.road_lights.color = color
        color, t = self.track.get_value(EventType.RIGHT_LASERS, ms_time)
        self.right_lasers.color = color
        color, t = self.track.get_value(EventType.LEFT_LASERS, ms_time)
        self.left_lasers.color = color
        color, t = self.track.get_value(EventType.BACK_LASERS, ms_time)
        self.back_lasers.color = color
        color, t = self.track.get_value(EventType.RING_LIGHTS, ms_time)
        self.ring_lights.color = color


class BeatSaber(moderngl_window.WindowConfig):
    title = "Beat Saber Light Show"
    resource_dir = './resources'
    window_size = 1920, 1080

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.bpm = 242  # Hardcode bpm from info.dat
        self.camera = KeyboardCamera(self.wnd.keys, near=1.0, far=1000.0)
        self.camera.velocity = 50
        self.camera_enabled = True

        self.map = BeatSaberMap(
            self.load_scene('bs_map.glb'),
            BSTrack('./resources/Lightshow.dat'),
        )
        self.music_player = Player()
        self.music_source = StaticSource(load('./resources/megalovania.wav'))
        self.music_player.queue(self.music_source)
        self.music_player.play()

    def render(self, time, frame_time):
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        # self.wnd.clear(0.25, 0.25, 0.25)
        self.map.render(self.camera, time, frame_time)

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
