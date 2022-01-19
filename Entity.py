import Physics
import pygame
import Settings


class Entity:
    def __init__(self, x, y, object, width, height, screen, name):
        self._startX, self._startY = x, y
        self._name = name
        self._Physic = Physics.Physic.Physic(isGravity=True)
        self._Collider = Physics.Collider.Collider(
            width, height, x=self._startX, y=self._startY, object=object
        )
        self.screen = screen

    def Move(self, up, left, right, blocks):
        if up:
            if self._Physic._onGround:
                self._Physic._onGround = False
                self._Physic.AddForce([0, -Physics.PhysicSettings.JUMP_POWER])

        if left:
            self._Physic.AddForce([-Physics.PhysicSettings.MOVE_SPEED, 0])

        if right:
            self._Physic.AddForce([Physics.PhysicSettings.MOVE_SPEED, 0])

        self._Physic.gravity()
        self._Physic._onGround = False

        self._Collider.MoveY(self._Physic._yVelocity)

        self._Collider.OnCollisionEnter(
            self._Collider.CollisionMove,
            [0, self._Physic._yVelocity],
            self._Physic,
            blocks,
        )

        self._Collider.MoveX(self._Physic._xVelocity)

        self._Collider.OnCollisionEnter(
            self._Collider.CollisionMove,
            [self._Physic._xVelocity, 0],
            self._Physic,
            blocks,
        )
        self._Physic._xVelocity = 0

    def Debug(self):
        print("Name:", self._name)
        print(
            f"Physics: \n OnGround {self._Physic._onGround} \n velocity: {self._Physic.Velocities}"
        )
        print(f"Position: \n {self._Collider.Position}")

    def DrawHitBoxs(self):
        pygame.draw.rect(self.screen, Settings.GREEN, self._Collider._Rect, 2)
