from Generation import Chunk, GenerationSettings
from Generation.Block import Block
from HeightMap import HeightMap
import Player

import pygame
import sys
import Settings
import Generation
import multiprocessing
from Generation import Blocks
def main():
    pygame.init()

    screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    entities = pygame.sprite.Group()
    player = Player.Player(Settings.WIDTH // 2, Settings.HEIGHT // 2, screen)

    heightMap = HeightMap()
    heightMap.Generate(1)
    startChunk = Generation.Chunk.Chunk([2, 8], player, screen)
    startChunk.Generate(screen, heightMap)
    entities.add(startChunk.listBlocks)
    entities.add(player)
    player.chunk = startChunk
    visibleChunks = [startChunk]

    timer = pygame.time.Clock()
    
    if True:
        while True:

            screen.fill((0,0,0))
            playerPos = player.Position

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if event.button == 3 or event.button == 1:
                        mouseClick = pygame.mouse.get_pos()
                        distX, distY = mouseClick[0] - Settings.HALF_WIDTH, mouseClick[1] - Settings.HALF_HEIGHT
                        distX = distX // GenerationSettings.SIZEBLOCK
                        distY = distY // GenerationSettings.SIZEBLOCK
                        

                        playerBlockX = playerPos[0] // GenerationSettings.SIZEBLOCK
                        playerBlockY = playerPos[1] // GenerationSettings.SIZEBLOCK
                        blockCoords = [(playerBlockX + distX) * GenerationSettings.SIZEBLOCK, (playerBlockY + distY) * GenerationSettings.SIZEBLOCK]
                        
                        for chunk in visibleChunks:

                            if chunk.CheckCoordsInside(blockCoords):
                                if event.button == 3:
                                    
                                    block = Block(blockCoords[0], blockCoords[1], Blocks.EARTH, 1, screen)
                                    chunk.listBlocks.append(block)
                                    entities.add(block)
                                else:
                                    for block in chunk.listBlocks:
                                        print(block.Position, blockCoords)
                                        if block.Position[0] == blockCoords[0] and block.Position[1] == blockCoords[1]:
                                            print("deleted")
                                            chunk.listBlocks.remove(block)
                                            entities.remove(block)
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        player.right = True
                        player.directional = 1

                    if event.key == pygame.K_a:
                        player.left = True
                        player.directional = -1

                    if event.key == pygame.K_SPACE:
                        player.up = True


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        player.right = False

                    if event.key == pygame.K_a:
                        player.left = False

                    if event.key == pygame.K_SPACE:
                        player.up = False

            player.Update()
            chunk = player.chunk.GenerateNext(heightMap)

            if chunk:
                visibleChunks.append(chunk)
                entities.add(chunk.listBlocks)

            xOffset = Settings.HALF_WIDTH - playerPos[0]
            yOffset = Settings.HALF_HEIGHT - playerPos[1]
            for chunk in visibleChunks:

                if chunk.CheckCoordsInside(playerPos):
                    player.chunk = chunk
                if playerPos[0] > (chunk.positionStart[0] + GenerationSettings.BLOCKS_IN_CHUNK * 2) * GenerationSettings.SIZEBLOCK:
                    entities.remove(chunk.listBlocks)
                    visibleChunks.remove(chunk)
                    chunk.DestroyChunk()

                elif playerPos[0] < (chunk.positionStart[0] - GenerationSettings.BLOCKS_IN_CHUNK * 2) * GenerationSettings.SIZEBLOCK:
                    entities.remove(chunk.listBlocks)
                    visibleChunks.remove(chunk)
                    chunk.DestroyChunk()

                        
            for entity in entities:
                screen.blit(entity._Image, (entity.Position[0] + xOffset, entity.Position[1] + yOffset))        

            timer.tick(Settings.FPS)
            pygame.display.flip()
        

if __name__ == "__main__":
    main()