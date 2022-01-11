
class Physic():
    def __init__(self, isGravity: bool):
        self.mass = 1
        self._yVelocity, self._xVelocity = 0, 0
        if isGravity:
            self._onGround = False
    
    @property
    def Velocities(self):
        return [self._xVelocity, self._yVelocity]
        