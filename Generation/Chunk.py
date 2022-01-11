from typing import Set

from pygame.time import set_timer
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
        self.GeneratedNext = False

    def Generate(self, screen):
        x, y = self.positionStart
        for i in range(1, GenerationSettings.BLOCKS_IN_CHUNK + 1):
            block = Block.Block(x + self.player.directional * GenerationSettings.SIZEBLOCK * i, y, pygame.image.load("Sprites/Grass.jpg"), 1, screen)
            self.listBlocks.append(block)

    def CheckPLayerInside(self, playerPos):
        x, y = playerPos
        if x > self.positionStart[0] and x < self.positionStart[0] + GenerationSettings.NEXT:
            self.player.chunk = self

    def DestroyChunk(self):
        for i in self.listBlocks:
            i.kill()
        del self

    def GenerateNext(self, playerPos):
        if playerPos[0] > self.player.chunk.positionStart[0] + GenerationSettings.NEXT // (GenerationSettings.SIZEBLOCK * 2) and not self.GeneratedNext:
            oldPosition = self.player.chunk.positionStart
            self.GeneratedNext = True
            chunk = Chunk([oldPosition[0] + GenerationSettings.NEXT, oldPosition[1]], self.player, self.screen)
            chunk.Generate(self.screen)
            return chunk
        else:
            return False