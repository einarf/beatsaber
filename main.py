import math

import moderngl
import moderngl_window
from pyrr import Matrix44
from moderngl_window.scene.camera import KeyboardCamera
from track import BSTrack


class BeatSaberMap:

    def __init__(self, scene, track):
        self.scene = scene
        self.track = track

        # Objects & Materials
        self.mat_back_lights = self.scene.find_material(name="Back Lights")

        # Static unlit par of the map
        self.highway = self.scene.find_node(name="Highway")

        # Rings
        self.ring_01 = self.scene.find_node(name='Ring.001')
        self.ring_02 = self.scene.find_node(name='Ring.001')

        # Light rails on left and right side
        self.right_static = self.scene.find_node(name="Right Static")
        self.left_static = self.scene.find_node(name="Left Static")

    def render(self, camera, time, frame_time):
        self.mat_back_lights.color = math.fmod(time, 1.0), 0.0, 0.0, 1.0
        self.scene.draw(camera.projection.matrix, camera.matrix)


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

    def render(self, time, frame_time):
        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.CULL_FACE)
        self.wnd.clear(0.25, 0.25, 0.25)
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
