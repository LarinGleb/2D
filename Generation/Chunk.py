
from . import GenerationSettings
from . import Block
import pygame

from . import Blocks
import sys
sys.path.append("..")
import Changes
import numba

@numba.njit(fastmath = True)
def CalculateHeight(height):
    return int(height/10)

@numba.njit(fastmath = True)
def GetSprite(i):
    if i == 1:
        return 1
    elif i == 2:
        return 2
    elif i < 5 and i > 2:
        return 3
    elif i >= 5:
        return 4

class Chunk():
    def __init__(self, positionStart, player, screen):
        
        self.player = player
        self.positionStart = positionStart
        self.id = hash(sum(positionStart))
        self.listBlocks = []
        self.entity = []

        self.screen = screen
        self.GeneratedRight = False
        self.GeneratedLeft = False

    def Debug(self):
        pygame.draw.line(self.screen, )
    
    def __eq__(self, __o: object):
        return self.id == __o.id

    def Generate(self, screen, heightmap):
        
        x, y = self.positionStart
        for i in range(1, GenerationSettings.BLOCKS_IN_CHUNK + 1):
            currentY = CalculateHeight(heightmap.GetPixel(x + i))
            currentX = (x + i) * GenerationSettings.SIZEBLOCK
            for i in range(1, currentY):
                block = Block.Block(currentX, (currentY + i)*GenerationSettings.SIZEBLOCK, GetSprite(i), screen)
                self.listBlocks.append(block)
        self.ChangeChunk()

    def CheckCoordsInside(self, position):
        x, y = position
        return x > self.positionStart[0]  * GenerationSettings.SIZEBLOCK and x < (self.positionStart[0] + GenerationSettings.BLOCKS_IN_CHUNK) * GenerationSettings.SIZEBLOCK
            

    def DestroyChunk(self):
        for i in self.listBlocks:
            i.kill()
        del self

    def GetBlock(self, position):
        for block in self.listBlocks:
            if block.Position == position:
                return block

    def ChangeChunk(self):
        for change in Changes.FixChange.GetChanges():
            if self.CheckCoordsInside(change.block.Position):
                if change.type == 'break':
                    block = self.GetBlock(change.block.Position)
                    if block in self.listBlocks:
                        self.listBlocks.remove(block)
                    
                if change.type == 'create':
                    self.listBlocks.append(change.block)

    def GenerateNext(self, heightmap):
        if self.player.directional == 1:
            if self.player.Position[0] > (self.player.chunk.positionStart[0] + GenerationSettings.BLOCKS_IN_CHUNK // 2 ) * GenerationSettings.SIZEBLOCK and not self.GeneratedRight:
                oldPosition = self.player.chunk.positionStart
                self.GeneratedRight = True
                chunk = Chunk([oldPosition[0] + self.player.directional * GenerationSettings.BLOCKS_IN_CHUNK, oldPosition[1]], self.player, self.screen)
                chunk.Generate(self.screen, heightmap)
                return chunk
            else:
                return False
        else:
            if self.player.Position[0] < (self.player.chunk.positionStart[0] + GenerationSettings.BLOCKS_IN_CHUNK) * GenerationSettings.SIZEBLOCK and not self.GeneratedLeft:
                oldPosition = self.player.chunk.positionStart
                self.GeneratedLeft = True
                chunk = Chunk([oldPosition[0] + self.player.directional * GenerationSettings.BLOCKS_IN_CHUNK, oldPosition[1]], self.player, self.screen)
                chunk.Generate(self.screen, heightmap)
                return chunk
            else:
                return False