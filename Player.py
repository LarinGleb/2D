
import pygame
import Entity
import Physics.PhysicSettings
import Settings

class Player(pygame.sprite.Sprite):
    def __init__(self, Xstart, Ystart, screen):
        
        pygame.sprite.Sprite.__init__(self)
        self._Entity = Entity.Entity(Xstart, Ystart, self, 64, 64, screen)
        self.screen = screen
        self._Image = pygame.image.load('Sprites/GraySqure.png')
        self.left = False
        self.right = False
        self.up = False
        self.chunk = None
        self.directional = 1

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
        
        if self.up:
            if self._Entity._Physic._onGround:
                self._Entity._Physic._onGround = False
                self._Entity._Physic._yVelocity = -Physics.PhysicSettings.JUMP_POWER
                
                 
        if self.left:
            self._Entity._Physic._xVelocity = -Physics.PhysicSettings.MOVE_SPEED 
 
        if self.right:
            self._Entity._Physic._xVelocity = Physics.PhysicSettings.MOVE_SPEED
            
        if not self._Entity._Physic._onGround:
            self._Entity._Physic._yVelocity += Physics.PhysicSettings.GRAVITY

        self._Entity._Physic._onGround = False

        self._Entity._Collider.MoveY(self._Entity._Physic._yVelocity)

        self._Entity._Collider.OnCollisionEnter([0, self._Entity._Physic._yVelocity], self._Entity._Physic, self.chunk.listBlocks)

        self._Entity._Collider.MoveX(self._Entity._Physic._xVelocity)

        self._Entity._Collider.OnCollisionEnter([self._Entity._Physic._xVelocity, 0], self._Entity._Physic, self.chunk.listBlocks)

        self._Entity._Physic._xVelocity = 0

    def Debug(self):
        
        print(f"Physics: \n OnGround {self._Entity._Physic._onGround} \n velocity: {self._Entity._Physic.Velocities}")
        print(f"Position: \n {self.Position}")
