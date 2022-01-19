from ast import arg
from select import select
import pygame
from Changes.FixChange import Append
import Entity
import Physics.PhysicSettings
import Settings
from Inventory import Item


class Player(pygame.sprite.Sprite):
    def __init__(self, Xstart, Ystart, screen):

        pygame.sprite.Sprite.__init__(self)
        self._Entity = Entity.Entity(Xstart, Ystart, self, 64, 64, screen, "Player")
        self.screen = screen
        self._Image = pygame.image.load("Sprites/GraySqure.png")
        self.left = False
        self.right = False
        self.up = False
        self.chunk = None
        self.chooseCell = None
        self.directional = 1
        self.inventory = ""

    @property
    def rect(self):
        return self._Entity._Collider._Rect

    @property
    def image(self):
        return self._Image

    @property
    def Position(self):
        return self._Entity._Collider.Position

    def Update(self):
        self._Entity.Move(self.up, self.left, self.right, self.chunk.listBlocks)

    def TryItemAppend(self):
        return self._Entity._Collider.CollisionGet(self.chunk.entity)

    def Debug(self):

        self._Entity.Debug()
        print(f"ChunkCoords \n", self.chunk.positionStart)
