from ast import arg
import pygame
from . import Physic


class Collider:
    def __init__(self, width: int, height: int, x: float, y: float, object):
        self._Width = width
        self._selfObject = object
        self._Height = height
        self._Rect = pygame.Rect(x, y, width, height)

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

    def OnTriggerEnter(self, function, *args):
        function(*args)

    def OnCollisionEnter(self, function, *args):
        function(*args)

    def CollisionGet(self, objects):
        for object in objects:
            if self._Rect.colliderect(object._Entity._Collider._Rect):
                return object
                break

    def CollisionCheck(self, objects, function, *args):
        for object in objects:
            if self._Rect.colliderect(object._Entity._Collider._Rect):
                function(*args, object)

    def CollisionMove(self, velocities, physic: Physic, objects: list):
        self.CollisionCheck(objects, self.Push, velocities[0], velocities[1], physic)

    def Push(self, xVelocity, yVelocity, physic: Physic, object):

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
