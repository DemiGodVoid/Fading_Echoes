from panda3d.core import Point3, GeomVertexFormat, GeomVertexData, Geom, GeomNode, GeomVertexWriter, GeomTriangles, Texture, TransparencyAttrib, CollisionTraverser
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import health
from punch import Puncher
from barrier import Barrier
from place import BlockPlacer
import math

class Game(ShowBase):
    def __init__(self):
        super().__init__()

        self.cTrav = CollisionTraverser()
        self.disable_mouse()

        self.camera.set_pos(0, -20, 10)
        self.camera.look_at(0, 0, 2)
        self.set_background_color(0.53, 0.81, 0.92)

        self.create_ground()

        self.speed = 40
        self.rotation_step = 2

        self.task_mgr.add(self.update, "update")

        self.arms = self.on_screen_arms()
        self.is_punching = False

        self.health_display = health.HealthDisplay(self)
        self.block_placer = BlockPlacer(self, self.camera)
        self.puncher = Puncher(self, self.block_placer)
        self.barrier = Barrier(self, self.camera)

        self.accept('e', self.start_punch)

        self.cTrav.show_collisions(self.render)

    def on_screen_arms(self):
        arms_texture = self.loader.load_texture("textures/arms.png")
        arms_texture.set_minfilter(Texture.FT_nearest)
        arms_texture.set_magfilter(Texture.FT_nearest)
        arms_texture.set_wrap_u(Texture.WM_clamp)
        arms_texture.set_wrap_v(Texture.WM_clamp)

        arms_image = OnscreenImage(image='textures/arms.png', pos=(0, 0, -0.6), scale=(1.5, 1, 0.5))
        arms_image.set_texture(arms_texture)
        arms_image.set_transparency(TransparencyAttrib.M_alpha)
        return arms_image

    def start_punch(self):
        if not self.is_punching:
            self.is_punching = True
            self.puncher.punch()
            self.task_mgr.add(self.punch_animation, "punch_animation")

    def punch_animation(self, task):
        progress = task.time * 5
        if progress < 0.5:
            self.arms.set_pos(0, 0, -0.6 - progress * 0.5)
        elif progress < 1.0:
            self.arms.set_pos(0, 0, -0.85 + (progress - 0.5) * 0.5)
        else:
            self.arms.set_pos(0, 0, -0.6)
            self.is_punching = False
            return Task.done
        return Task.cont

    def create_ground(self):
        texture = self.loader.load_texture("textures/ground.png")
        block_size = 10
        for x in range(-50, 51):
            for y in range(-50, 51):
                self.create_block(x * block_size, y * block_size, -0.5, block_size, texture)

    def create_block(self, x, y, z, size, texture):
        vertex_format = GeomVertexFormat.get_v3n3t2()
        vertex_data = GeomVertexData('block', vertex_format, Geom.UHStatic)

        vertex_writer = GeomVertexWriter(vertex_data, 'vertex')
        normal_writer = GeomVertexWriter(vertex_data, 'normal')
        texcoord_writer = GeomVertexWriter(vertex_data, 'texcoord')

        half_size = size / 2
        vertices = [
            Point3(-half_size, -half_size, 0),
            Point3(half_size, -half_size, 0),
            Point3(half_size, half_size, 0),
            Point3(-half_size, half_size, 0)
        ]

        for v in vertices:
            vertex_writer.add_data3f(v.x, v.y, v.z)
            normal_writer.add_data3f(0, 0, 1)

        texcoord_writer.add_data2f(0, 0)
        texcoord_writer.add_data2f(1, 0)
        texcoord_writer.add_data2f(1, 1)
        texcoord_writer.add_data2f(0, 1)

        faces = [(0, 1, 2), (0, 2, 3)]

        geom = Geom(vertex_data)
        triangles = GeomTriangles(Geom.UHStatic)
        for face in faces:
            triangles.add_vertices(face[0], face[1], face[2])
        geom.add_primitive(triangles)

        node = GeomNode('block')
        node.add_geom(geom)
        block = self.render.attach_new_node(node)
        block.set_pos(x, y, z)
        block.set_texture(texture)

    def update(self, task):
        dt = self.clock.get_dt()

        if self.mouseWatcherNode.is_button_down('w'):
            forward_direction = self.camera.get_quat().get_forward()
            forward_direction.set_z(0)
            forward_direction.normalize()
            self.camera.set_pos(self.camera.get_pos() + forward_direction * self.speed * dt)

        if self.mouseWatcherNode.is_button_down('s'):
            backward_direction = self.camera.get_quat().get_forward()
            backward_direction.set_z(0)
            backward_direction.normalize()
            self.camera.set_pos(self.camera.get_pos() - backward_direction * self.speed * dt)

        if self.mouseWatcherNode.is_button_down('a'):
            left_direction = self.camera.get_quat().get_right()
            left_direction.set_z(0)
            left_direction.normalize()
            self.camera.set_pos(self.camera.get_pos() - left_direction * self.speed * dt)

        if self.mouseWatcherNode.is_button_down('d'):
            right_direction = self.camera.get_quat().get_right()
            right_direction.set_z(0)
            right_direction.normalize()
            self.camera.set_pos(self.camera.get_pos() + right_direction * self.speed * dt)

        if self.mouseWatcherNode.is_button_down('i'):
            self.camera.set_h(self.camera.get_h() - self.rotation_step)
        if self.mouseWatcherNode.is_button_down('o'):
            new_pitch = self.camera.get_p() + self.rotation_step
            self.camera.set_p(max(min(new_pitch, 80), -80))
        if self.mouseWatcherNode.is_button_down('p'):
            self.camera.set_h(self.camera.get_h() + self.rotation_step)
        if self.mouseWatcherNode.is_button_down('l'):
            new_pitch = self.camera.get_p() - self.rotation_step
            self.camera.set_p(max(min(new_pitch, 80), -80))

        if self.camera.get_z() < 0:
            self.camera.set_z(0)

        return Task.cont

if __name__ == "__main__":
    game = Game()
    game.run()
