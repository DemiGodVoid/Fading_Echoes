import numpy as np
from direct.task import Task
from panda3d.core import Point3
from panda3d.core import CollisionTraverser, CollisionNode, CollisionRay, CollisionHandlerQueue
from panda3d.core import KeyboardButton

class BlockPlacer:
    def __init__(self, game, camera):
        self.game = game
        self.camera = camera
        self.blocks = []
        self.block_texture = self.game.loader.load_texture("es.png")
        self.accept_input()

    def accept_input(self):
        self.game.accept("r", self.place_block)

    def place_block(self):
        cam_pos = self.camera.get_pos(self.game.render)
        cam_forward = self.camera.get_quat(self.game.render).get_forward()

        # Place block 5 units in front of where the camera is looking
        target_pos = cam_pos + cam_forward * 5

        block = self.create_block(target_pos)
        self.blocks.append(block)

    def create_block(self, pos):
        block = self.game.loader.load_model("models/box")
        block.reparent_to(self.game.render)
        block.set_pos(pos)
        block.set_texture(self.block_texture, 1)
        return block
