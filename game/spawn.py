import numpy as np
from direct.task import Task
from panda3d.core import Point3
from random import uniform

class Spawner:
    def __init__(self, game, camera):
        self.game = game
        self.camera = camera
        self.spawn_interval = 10  # seconds
        self.spawn_radius = 10  # 10 units away from the player
        self.creatures = []  # List to track active creatures
        self.spawn_task = self.game.task_mgr.do_method_later(self.spawn_interval, self.spawn_square, "spawn_square")
    
    def spawn_square(self, task):
        # Get the camera's position to spawn the square nearby but not on the player
        player_position = self.camera.get_pos()

        # Randomly spawn the square at a location 10 units away from the player in a random direction
        angle = uniform(0, 360)  # Random angle for spawning
        spawn_x = player_position.x + self.spawn_radius * np.cos(np.radians(angle))
        spawn_y = player_position.y + self.spawn_radius * np.sin(np.radians(angle))

        # Create a new square at the spawn location
        square = self.create_square(spawn_x, spawn_y, player_position.z)
        self.creatures.append(square)  # Add the new creature to the list

        # Return the task to continue calling spawn_square every interval
        return Task.again

    def create_square(self, x, y, z):
        # Create a simple square model that moves towards the player
        square = self.game.loader.load_model("models/box")  # Ensure you have a basic box model
        square.reparent_to(self.game.render)
        square.set_pos(x, y, z)
        
        # Set a speed for the square to move towards the player
        square.set_tag("moving_towards_player", "true")

        # Make the square move towards the player every frame
        self.game.task_mgr.add(self.move_towards_player, "move_towards_player", extraArgs=[square], appendTask=True)
        return square  # Return the created square

    def move_towards_player(self, square, task):
        # Check if the square exists and has not been removed from the scene graph
        if not square or square.is_empty():
            return Task.done  # Stop the task if the square no longer exists

        # Get the position of the player (camera)
        player_position = self.camera.get_pos()

        # Move the square towards the player
        direction = player_position - square.get_pos()
        direction.normalize()
        square.set_pos(square.get_pos() + direction * 0.1)  # Speed of movement

        # If the square reaches the player, remove it
        if (square.get_pos() - player_position).length() < 1:
            print("Creature reached the player!")
            square.remove_node()  # Remove the square once it reaches the player
            if square in self.creatures:
                self.creatures.remove(square)  # Remove from list
            return Task.done

        return Task.cont
