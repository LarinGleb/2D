
import sys
sys.path.append("..")
import pygame
import Entity
from Generation import GenerationSettings
typesItem = {
    'block' : 99,
    'tool' : 1
}
SIZEBLOCKITEM = GenerationSettings.SIZEBLOCK // 2

class Item(pygame.sprite.Sprite):
    def __init__(self, id, typeItem, spriteItem, position, chunkWhere, screen):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.maxCount = typesItem[typeItem]
        self.blocks = chunkWhere.listBlocks
        self.chunk = chunkWhere
        self._Image = pygame.transform.scale(spriteItem, (SIZEBLOCKITEM, SIZEBLOCKITEM))
        self._Entity = Entity.Entity(position[0], position[1], self, SIZEBLOCKITEM, SIZEBLOCKITEM, screen, "Item")

    def Update(self):
        self._Entity.Move(False, False, False, self.blocks)
    
    @property
    def Position(self):
        return self._Entity._Collider.Position