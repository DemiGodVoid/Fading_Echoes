from panda3d.core import Point3

class Puncher:
    def __init__(self, game, spawner):
        self.game = game
        self.spawner = spawner

    def punch(self):
        player_position = self.game.camera.get_pos()
        punch_range = 3
        forward = self.game.camera.get_quat().get_forward()
        for creature in list(self.spawner.creatures):
            to_creature = creature.get_pos() - player_position
            distance = to_creature.length()
            if distance <= punch_range:
                to_creature.normalize()
                dot = forward.dot(to_creature)
                if dot > 0.7:
                    print(f"Punched creature at {creature.get_pos()}")
                    creature.remove_node()
                    self.spawner.creatures.remove(creature)
