import pygame
from . import Physic

class Collider():
    def __init__(self, width: int, height: int, x: float, y: float, object,  isTrigger = False, ):
        self._Width = width
        self._selfObject = object
        self._Height = height
        self._Rect = pygame.Rect(x, y, width, height)
        self._isTrigger = isTrigger
        
    @property
    def Position(self):
        return [self._Rect.x, self._Rect.y]

    def MoveCollider(self, newPostion: list):
        newX, newY = newPostion
        self.MoveX(newX)
        self.MoveY(newY)

    def MoveX(self, xPos: float):
        self._Rect.x += xPos

    def MoveY(self, yPos: float):
        self._Rect.y += yPos
        

    def OnTriggerEnter(self, object, function):
        if self.object.collide_rect(self, object):
            function()

    def OnCollisionEnter(self, velocities, physic: Physic, objects: list):
        xVelocity, yVelocity = velocities

        for object in objects:
            
            
            if self._Rect.colliderect(object._Entity._Collider._Rect):

                if xVelocity > 0:
                    self._Rect.right = object._Entity._Collider._Rect.left

                if xVelocity < 0:
                    self._Rect.left = object._Entity._Collider._Rect.right

                if yVelocity > 0:
                    self._Rect.bottom = object._Entity._Collider._Rect.top
                    physic._onGround = True
                    physic._yVelocity = 0

                if yVelocity < 0:
                    self._Rect.top = object._Entity._Collider._Rect.bottom
                    physic._yVelocity = 0