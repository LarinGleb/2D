import Physics
import pygame
import Settings

class Entity():
    def __init__(self, x, y, object, width, height, screen):
        self._startX, self._startY = x, y
        self._Physic = Physics.Physic.Physic(isGravity = True)
        self._Collider = Physics.Collider.Collider(width, height, x = self._startX, y = self._startY, object = object)
        self.screen = screen

    def DrawHitBoxs(self):
        pygame.draw.rect(self.screen, Settings.GREEN, self._Collider._Rect, 2)