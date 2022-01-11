

import pygame
from . import GenerationSettings
import sys
sys.path.append("../Entity")
import Entity

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, image, id, screen):
        self.Sprite = pygame.sprite.Sprite.__init__(self)
        
        self._Image = image
        self._Entity = Entity.Entity(x, y, self, GenerationSettings.SIZEBLOCK, GenerationSettings.SIZEBLOCK, screen)
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
