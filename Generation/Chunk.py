from typing import Set


from . import GenerationSettings
from . import Block
import pygame

import sys
sys.path.append("../Sprites")



class Chunk():
    def __init__(self, positionStart, player, screen):
        self.player = player
        self.positionStart = positionStart
        self.listBlocks = []
        self.screen = screen
        self.GeneratedRight = False
        self.GeneratedLeft = False

    def Debug(self):
        pygame.draw.line(self.screen, )
    def CalculateHeight(self, height):
        return int(height/10)

    def Generate(self, screen, heightmap):
        
        x, y = self.positionStart
        for i in range(1, GenerationSettings.BLOCKS_IN_CHUNK + 1):
            block = Block.Block(x + GenerationSettings.SIZEBLOCK * i, self.CalculateHeight(heightmap.GetPixel(x+i)) * GenerationSettings.SIZEBLOCK, pygame.image.load("Sprites/Grass.jpg"), 1, screen)
            self.listBlocks.append(block)

    def CheckPLayerInside(self):
        x, y = self.player.Position
        if x > self.positionStart[0] and x < self.positionStart[0] + GenerationSettings.NEXT:
            self.player.chunk = self

    def DestroyChunk(self):
        for i in self.listBlocks:
            i.kill()
        del self

    def GenerateNext(self, heightmap):
        if self.player.directional == 1:
            if self.player.Position[0] > self.player.chunk.positionStart[0] + GenerationSettings.NEXT // (GenerationSettings.SIZEBLOCK * 2) and not self.GeneratedRight:
                oldPosition = self.player.chunk.positionStart
                self.GeneratedRight = True
                chunk = Chunk([oldPosition[0] + self.player.directional * GenerationSettings.NEXT, oldPosition[1]], self.player, self.screen)
                chunk.Generate(self.screen, heightmap)
                return chunk
            else:
                return False
        else:
            if self.player.Position[0] < self.player.chunk.positionStart[0] + GenerationSettings.NEXT and not self.GeneratedLeft:
                oldPosition = self.player.chunk.positionStart
                self.GeneratedLeft = True
                chunk = Chunk([oldPosition[0] + self.player.directional * GenerationSettings.NEXT, oldPosition[1]], self.player, self.screen)
                chunk.Generate(self.screen, heightmap)
                return chunk
            else:
                return False