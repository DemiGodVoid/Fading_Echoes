from panda3d.core import Point3

class Puncher:
    def __init__(self, game, spawner):
        """
        Initialize the Puncher class.
        :param game: The main game instance.
        :param spawner: The Spawner instance to manage spawned entities.
        """
        self.game = game
        self.spawner = spawner

    def punch(self):
        """
        Handles the punch action. Checks if any creatures are within range and removes them.
        """
        player_position = self.game.camera.get_pos()
        punch_range = 3  # Range in which creatures are affected by the punch

        # Loop through all creatures in the spawner's list and remove those in range
        for creature in self.spawner.creatures:
            if (creature.get_pos() - player_position).length() <= punch_range:
                print(f"Punched creature at {creature.get_pos()}")
                creature.remove_node()
                self.spawner.creatures.remove(creature)
