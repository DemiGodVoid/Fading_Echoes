import numpy as np
from direct.task import Task
from panda3d.core import Point3, Texture
from random import uniform

class Spawner:
    def __init__(self, game, camera):
        self.game = game
        self.camera = camera
        self.spawn_interval = 10
        self.spawn_radius = 10
        self.creatures = []
        self.spawn_task = self.game.task_mgr.do_method_later(self.spawn_interval, self.spawn_square, "spawn_square")
        self.enemy_texture = self.game.loader.load_texture("es.png")

    def spawn_square(self, task):
        player_position = self.camera.get_pos()
        angle = uniform(0, 360)
        spawn_x = player_position.x + self.spawn_radius * np.cos(np.radians(angle))
        spawn_y = player_position.y + self.spawn_radius * np.sin(np.radians(angle))
        square = self.create_square(spawn_x, spawn_y, player_position.z)
        self.creatures.append(square)
        return Task.again

    def create_square(self, x, y, z):
        square = self.game.loader.load_model("models/box")
        square.reparent_to(self.game.render)
        square.set_pos(x, y, z)
        square.set_texture(self.enemy_texture, 1)
        square.set_tag("moving_towards_player", "true")
        self.game.task_mgr.add(self.move_towards_player, "move_towards_player", extraArgs=[square], appendTask=True)
        return square

    def move_towards_player(self, square, task):
        if not square or square.is_empty():
            return Task.done
        player_position = self.camera.get_pos()
        direction = player_position - square.get_pos()
        direction.normalize()
        square.set_pos(square.get_pos() + direction * 0.1)
        if (square.get_pos() - player_position).length() < 1:
            print("Creature reached the player!")
            square.remove_node()
            if square in self.creatures:
                self.creatures.remove(square)
            return Task.done
        return Task.cont
