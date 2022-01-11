from Generation import Chunk, GenerationSettings
import Player

import pygame
import sys
import Settings
import Generation

def main():
    pygame.init()

    screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    entities = pygame.sprite.Group()
    player = Player.Player(Settings.WIDTH // 2, Settings.HEIGHT // 2, screen)

    

    startChunk = Generation.Chunk.Chunk([2 * 64, 8 * 64], player, screen)
    startChunk.Generate(screen)
    entities.add(startChunk.listBlocks)
    entities.add(player)
    

    player.chunk = startChunk
    visibleChunks = [startChunk]
    timer = pygame.time.Clock()
    

    while True:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()

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
        playerPos = player.Position
        chunk = player.chunk.GenerateNext(playerPos)
        if chunk:
            visibleChunks.append(chunk)
            entities.add(chunk.listBlocks)
        
        xOffset = Settings.HALF_WIDTH - playerPos[0]
        yOffset = Settings.HALF_HEIGHT - playerPos[1]

        for chunk in visibleChunks:
            chunk.CheckPLayerInside(playerPos)
            if playerPos[0] > chunk.positionStart[0] + GenerationSettings.NEXT * 2 + Settings.VIEW_BLOCKS * GenerationSettings.SIZEBLOCK:
                entities.remove(chunk.listBlocks)
                visibleChunks.remove(chunk)
                chunk.DestroyChunk()
       
        print(player.chunk.positionStart)
        for entity in entities:
            screen.blit(entity._Image, (entity.Position[0] + xOffset, entity.Position[1] + yOffset))
        

        timer.tick(Settings.FPS)
        pygame.display.flip()
        

if __name__ == "__main__":
    main()