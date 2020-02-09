import math
from pathlib import Path
from pyrr import matrix44

from moderngl_window import resources
from moderngl_window.meta import ProgramDescription, DataDescription
from track import  EventType

RESOURCE_DIR = Path(__file__).parent.resolve() / 'resources'
resources.register_dir(RESOURCE_DIR)


class BSScene:

    def __init__(self, scene, camera, track):
        self.scene = scene
        self.track = track
        self.camera = camera

        static_color = 0.01, 0.01, 0.01, 1.0

        # light/laser shaders
        self.light_static_prog = resources.programs.load(ProgramDescription(path='programs/light_static.glsl'))
        self.laser_prog = resources.programs.load(ProgramDescription(path='programs/laser.glsl'))

        self.highway = self.scene.find_node('Highway')
        self.highway.mesh.material.color = static_color

        # Inner rings
        self.inner_ring_prog = resources.programs.load(ProgramDescription(path='programs/inner_rings.glsl'))
        self.inner_ring_prog['color'] = static_color
        self.inner_ring_prog['ring_spacing'] = -5.0

        self.inner_ring_vao = self.scene.find_node('Ring.001').mesh.vao

        # Outer rings
        self.outer_ring_prog = resources.programs.load(ProgramDescription(path='programs/outer_rings.glsl'))        
        self.outer_ring_prog['color'] = static_color
        self.outer_ring_vao = self.scene.find_node('Ring.021').children[1].mesh.vao

        # Ring neons
        self.ring_neon_prog = resources.programs.load(ProgramDescription(path='programs/outer_rings_neons.glsl'))        
        self.ring_neon_1 = self.scene.find_node('Ring.021').children[0].mesh.vao
        self.ring_neon_2 = self.scene.find_node('Ring.021').children[2].mesh.vao
        self.ring_neon_3 = self.scene.find_node('Ring.021').children[3].mesh.vao
        self.ring_neon_4 = self.scene.find_node('Ring.021').children[4].mesh.vao

        # Lights
        self.light_left_static_vao = self.scene.find_node('Left Static').mesh.vao
        self.light_right_static_vao = self.scene.find_node('Right Static').mesh.vao
        self.light_center_static_vao = self.scene.find_node('Center Lights').mesh.vao
        self.light_back_static_vao = self.scene.find_node('Back Lights').mesh.vao

        # Lasers
        self.laser_left_1 = self.scene.find_node('Left 1').mesh.vao
        self.laser_right_1 = self.scene.find_node('Right 1').mesh.vao

        # Color variables for each light
        self.light_center_color = 0, 0, 0, 0
        self.light_back_color = 0, 0, 0, 0
        self.laser_left_color = 0, 0, 0, 0
        self.laser_right_color = 0, 0, 0, 0
        self.light_ring_color = 0, 0, 0, 0

        # Ring values
        self.inner_rings_timestamp = 0
        self.inner_rings_rotation = 0
        self.inner_rings_velocity = 0
        self.inner_ring_spacing = -5

        # Moving lasers
        self.left_laser_rot = 0
        self.right_laser_rot = 0

        self.resize()

    def render(self, camera, time, frame_time):
        """Custom render method to gain exact control over the scene"""
        self.process_events(time, frame_time)
        cam = camera.matrix
        translate = matrix44.create_from_translation((0, -2, -10), dtype='f4')
        cam = matrix44.multiply(translate, cam)

        # Draw static geometry with default scene shader
        self.highway.draw(projection_matrix=camera.projection.matrix, camera_matrix=cam)

        # Inner rings
        self.inner_ring_prog['m_cam'].write(cam)
        self.inner_ring_prog['rotation'] = self.inner_rings_rotation
        self.inner_ring_prog['ring_spacing'] = self.inner_ring_spacing
        self.inner_ring_vao.render(self.inner_ring_prog, instances=20)

        # Outer rings
        self.outer_ring_prog['m_cam'].write(cam)
        self.outer_ring_prog['rotation'] = -self.inner_rings_rotation
        self.outer_ring_vao.render(self.outer_ring_prog, instances=11)

        # Ring neons
        self.ring_neon_prog['m_cam'].write(cam)
        self.ring_neon_prog['rotation'] = -self.inner_rings_rotation
        self.ring_neon_prog['color'] = self.light_ring_color
        self.ring_neon_1.render(self.ring_neon_prog, instances=11)
        self.ring_neon_2.render(self.ring_neon_prog, instances=11)
        self.ring_neon_3.render(self.ring_neon_prog, instances=11)
        self.ring_neon_4.render(self.ring_neon_prog, instances=11)

        # Light - static
        self.light_static_prog['m_cam'].write(cam)
        self.light_static_prog['color'] = self.laser_left_color
        self.light_left_static_vao.render(self.light_static_prog)
        self.light_static_prog['color'] = self.laser_right_color
        self.light_right_static_vao.render(self.light_static_prog)
        self.light_static_prog['color'] = self.light_center_color
        self.light_center_static_vao.render(self.light_static_prog)
        self.light_static_prog['color'] = self.light_back_color
        self.light_back_static_vao.render(self.light_static_prog)

        # Light - Moving lasers
        self.laser_prog['m_cam'].write(cam)
        self.laser_prog['color'] = self.laser_left_color
        self.laser_prog['rotation'] = self.left_laser_rot
        self.laser_prog['time'] = time
        self.laser_left_1.render(self.laser_prog, instances=4)
        self.laser_prog['color'] = self.laser_right_color
        self.laser_prog['rotation'] = self.right_laser_rot
        self.laser_right_1.render(self.laser_prog, instances=4)

    def resize(self):
        self.inner_ring_prog['m_proj'].write(self.camera.projection.matrix)
        self.outer_ring_prog['m_proj'].write(self.camera.projection.matrix)
        self.light_static_prog['m_proj'].write(self.camera.projection.matrix)
        self.laser_prog['m_proj'].write(self.camera.projection.matrix)
        self.ring_neon_prog['m_proj'].write(self.camera.projection.matrix)

    def process_events(self, time, frame_time):
        frame_time = min(abs(frame_time), 0.1)
        ms_time = int(time * 1000)

        # Lights and lasers
        color, t = self.track.get_value(EventType.ROAD_LIGHTS, ms_time)
        self.light_center_color = color
        color, t = self.track.get_value(EventType.BACK_LASERS, ms_time)
        self.light_back_color = color
        color, t = self.track.get_value(EventType.RING_LIGHTS, ms_time)
        self.light_ring_color = color
        color, t = self.track.get_value(EventType.RIGHT_LASERS, ms_time)
        self.laser_right_color = color
        color, t = self.track.get_value(EventType.LEFT_LASERS, ms_time)
        self.laser_left_color = color

        # Ring zoom
        time, value = self.track.get_value(EventType.RINGS_ZOOM, ms_time)
        self.inner_ring_spacing = -5 + value * 2

        # Inner/Outer Rings
        time, _ = self.track.get_value(EventType.RINGS_ROTATE, ms_time)
        if time != self.inner_rings_timestamp:
            self.inner_rings_timestamp = time
            if self.inner_rings_velocity < 0.5:
                self.inner_rings_velocity = 2.5
            else:
                self.inner_rings_velocity = -2.5

        self.inner_rings_rotation += self.inner_rings_velocity * frame_time / 3
        if self.inner_rings_velocity > 0:
            self.inner_rings_velocity = max(self.inner_rings_velocity - frame_time, 0)
        elif self.inner_rings_velocity < 0:
            self.inner_rings_velocity = min(self.inner_rings_velocity - frame_time, 0)

        # Moving left / right lasers
        time, value = self.track.get_value(EventType.LEFT_LASERS_SPEED, ms_time)
        self.left_laser_rot = math.sin(ms_time * value * 0.5 / 1000) * 0.5

        time, value = self.track.get_value(EventType.RIGHT_LASERS_SPEED, ms_time)
        self.right_laser_rot = math.sin(ms_time * -value * 0.5 / 1000) * 0.5
