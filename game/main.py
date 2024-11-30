from panda3d.core import Point3, GeomVertexFormat, GeomVertexData, Geom, GeomNode, GeomVertexWriter, GeomTriangles, Texture, TransparencyAttrib, CollisionTraverser, CollisionNode, CollisionRay, CollisionHandlerQueue, CollisionSphere
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import health  # Import the health module
import pause  # Pause menu to quit the game
from punch import Puncher  # Import the Puncher class
from barrier import Barrier  # Import the Barrier class
from spawn import Spawner  # Import the Spawner class

class Game(ShowBase):
    def __init__(self):
        super().__init__()

        # Initialize collision traverser
        self.cTrav = CollisionTraverser()  # Create the CollisionTraverser instance

        # Disable mouse control and lock the cursor in the center
        self.disable_mouse()

        # Set the cursor position to the center and lock it
        self.win.move_pointer(0, self.win.get_x_size() // 2, self.win.get_y_size() // 2)

        # Camera control settings
        self.camera.set_pos(0, -20, 10)  # Start camera a bit further away
        self.camera.look_at(0, 0, 2)

        # Add blue sky (background)
        self.set_background_color(0.53, 0.81, 0.92)  # Light blue color for sky

        # Create ground blocks (Minecraft-style grid)
        self.create_ground()

        # Movement settings
        self.speed = 40  # Movement speed (faster)
        self.sensitivity = 7.5  # 5x faster sensitivity for mouse look

        # Mouse movement task
        self.mouseTask = self.task_mgr.add(self.mouse_control_task, "mouse_control")

        # Task to update movement
        self.task_mgr.add(self.update, "update")

        # Display arms image with transparency
        self.arms = self.on_screen_arms()

        # Initialize the health display
        self.health_display = health.HealthDisplay(self)  # Initialize health display

        # Initialize the Pause Menu
        self.pause_menu = pause.PauseMenu(self)  # Create the pause menu object

        # Initialize the Spawner
        self.spawner = Spawner(self, self.camera)  # Pass the camera (player) to Spawner
       
        # Initialize the Puncher
        self.puncher = Puncher(self, self.spawner)  # Add the Puncher

        # Bind the 'E' key to the punch method
        self.accept('e', self.puncher.punch)

        # Initialize the Barrier, now passing self instead of self.base
        self.barrier = Barrier(self, self.camera) 
        
        # Enable collision debugging
        self.cTrav.show_collisions(self.render)  # Show collisions using the CollisionTraverser

    def on_screen_arms(self):
        try:
            # Load the texture for the arms with transparency handling
            arms_texture = self.loader.load_texture("textures/arms.png")

            if not arms_texture:
                print("Error: Failed to load arms.png!")
            else:
                print("Arms texture loaded successfully.")

            # Make sure the texture uses alpha (transparency)
            arms_texture.set_minfilter(Texture.FT_nearest)
            arms_texture.set_magfilter(Texture.FT_nearest)
            arms_texture.set_wrap_u(Texture.WM_clamp)
            arms_texture.set_wrap_v(Texture.WM_clamp)

            # Create an OnscreenImage to display the texture at the bottom of the screen
            arms_image = OnscreenImage(image='textures/arms.png', pos=(0, 0, -0.6), scale=(1.5, 1, 0.5))  # Scale adjusted

            # Set the transparent texture
            arms_image.set_texture(arms_texture)

            # Enable alpha transparency (don't make the image invisible)
            arms_image.set_transparency(TransparencyAttrib.M_alpha)

            return arms_image
        except Exception as e:
            print(f"Error displaying arms image: {e}")
            return None

    def create_ground(self):
        # Create an infinite grid of square blocks with ground.png texture
        texture = self.loader.load_texture("textures/ground.png")
        block_size = 10  # Size of each block (bigger than before for better visibility)

        for x in range(-50, 51):  # Range of blocks in X direction
            for y in range(-50, 51):  # Range of blocks in Y direction
                self.create_block(x * block_size, y * block_size, -0.5, block_size, texture)

    def create_block(self, x, y, z, size, texture):
        # Create a square block using Geom
        vertex_format = GeomVertexFormat.get_v3n3t2()  # Define format for vertex, normal, and texture coords
        vertex_data = GeomVertexData('block', vertex_format, Geom.UHStatic)

        vertex_writer = GeomVertexWriter(vertex_data, 'vertex')
        normal_writer = GeomVertexWriter(vertex_data, 'normal')
        texcoord_writer = GeomVertexWriter(vertex_data, 'texcoord')

        half_size = size / 2
        vertices = [
            Point3(-half_size, -half_size, 0),  # bottom-left
            Point3(half_size, -half_size, 0),   # bottom-right
            Point3(half_size, half_size, 0),    # top-right
            Point3(-half_size, half_size, 0)    # top-left
        ]

        for v in vertices:
            vertex_writer.add_data3f(v.x, v.y, v.z)
            normal_writer.add_data3f(0, 0, 1)  # Normal is pointing up

        texcoord_writer.add_data2f(0, 0)  # Bottom-left of texture
        texcoord_writer.add_data2f(1, 0)  # Bottom-right of texture
        texcoord_writer.add_data2f(1, 1)  # Top-right of texture
        texcoord_writer.add_data2f(0, 1)  # Top-left of texture

        faces = [
            (0, 1, 2), (0, 2, 3)  # two triangles to make the square
        ]

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

    def mouse_control_task(self, task):
        if self.mouseWatcherNode.has_mouse():
            mouse_x = self.mouseWatcherNode.get_mouse_x()
            mouse_y = self.mouseWatcherNode.get_mouse_y()

            self.camera.set_h(self.camera.get_h() - mouse_x * self.sensitivity)
            new_pitch = self.camera.get_p() + mouse_y * self.sensitivity
            if new_pitch > 80:
                self.camera.set_p(80)
            elif new_pitch < -80:
                self.camera.set_p(-80)
            else:
                self.camera.set_p(new_pitch)

            self.win.move_pointer(0, self.win.get_x_size() // 2, self.win.get_y_size() // 2)

        return Task.cont

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

        if self.camera.get_z() < 0:
            self.camera.set_z(0)

        return Task.cont


if __name__ == "__main__":
    game = Game()
    game.run()
