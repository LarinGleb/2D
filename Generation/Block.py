import pygame
from . import GenerationSettings
import sys

sys.path.append("..")
import Entity
from Inventory import Item
from . import Blocks


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, id, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self._Image = Blocks.idBlock[id]
        self._Entity = Entity.Entity(
            x,
            y,
            self,
            GenerationSettings.SIZEBLOCK,
            GenerationSettings.SIZEBLOCK,
            screen,
            "Block",
        )
        self._id = id

    @property
    def Position(self):
        return self._Entity._Collider.Position

    @property
    def rect(self):
        return self._Entity._Collider._Rect

    @property
    def image(self):
        return self._Image

    def GenerateItem(self, chunk):
        return Item.Item(
            self._id, "block", self.image, self.Position, chunk, self.screen
        )
