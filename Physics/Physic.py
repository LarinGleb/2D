from . import PhysicSettings


class Physic:
    def __init__(self, isGravity: bool):
        self.mass = 1
        self._yVelocity, self._xVelocity = 0, 0
        if isGravity:
            self._onGround = False

    @property
    def Velocities(self):
        return [self._xVelocity, self._yVelocity]

    def AddForce(self, vectorForce):
        xVel, yVel = vectorForce
        self._yVelocity += yVel
        self._xVelocity += xVel

    def gravity(self):
        if not self._onGround:
            self.AddForce([0, PhysicSettings.GRAVITY])
