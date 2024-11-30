from panda3d.core import CollisionNode, CollisionBox, Vec3, CollisionHandlerQueue, CollisionRay

class Barrier:
    def __init__(self, game, camera):
        self.game = game
        self.camera = camera
        
        # Load the visual model for the barrier (red box)
        self.barrier_model = self.game.loader.load_model("models/box")
        self.barrier_model.set_color(1, 0, 0, 1)  # Red color
        self.barrier_model.set_scale(2, 2, 2)  # Resize if needed
        self.barrier_model.set_pos(0, 10, 0)  # Position in front of the camera
        self.barrier_model.reparent_to(self.game.render)
        
        # Set up collision geometry (CollisionBox)
        self.collision_node = CollisionNode('barrier_collision')
        self.collision_box = CollisionBox(Vec3(0, 0, 0), 2, 2, 2)  # Create a larger collision box around the barrier
        self.collision_node.add_solid(self.collision_box)
        self.collision_node_path = self.barrier_model.attach_new_node(self.collision_node)
        
        # Initialize a collision handler for the camera
        self.collision_handler = CollisionHandlerQueue()

        # Create a collision ray from the camera
        self.camera_ray = CollisionRay()
        self.camera_ray.set_origin(self.camera.get_pos())
        self.camera_ray.set_direction(0, 0, -1)
        
        # Create a collision node for the camera
        self.camera_collision_node = CollisionNode("camera_ray")
        self.camera_collision_node.add_solid(self.camera_ray)
        self.camera_collision_path = self.camera.attach_new_node(self.camera_collision_node)
        
        # Add the camera ray to the collision traverser
        self.game.cTrav.add_collider(self.camera_collision_path, self.collision_handler)

        # Enable collision debugging
        self.game.cTrav.show_collisions(self.game.render)

        # Log the barrier info
        print("Barrier created and collisions enabled.")
        
    def check_collision(self):
        # Check for collision with the barrier by using the collision handler
        if self.collision_handler.get_num_entries() > 0:
            self.collision_handler.sort_entries()
            first_entry = self.collision_handler.get_entry(0)
            if first_entry.get_into_node().get_name() == "barrier_collision":
                return True
        return False
