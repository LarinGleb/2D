from fileinput import filename
from Generation import GenerationSettings
from Generation.Block import Block
from HeightMap import HeightMap
import Player

import pygame
import sys
import Settings
import Generation
import Changes
import Button
import os
import tkinter
import tkinter.filedialog
import Inventory

PATH = os.path.dirname(__file__)


def Path(save=False):
    global PATH
    tkTop = tkinter.Tk()
    tkTop.withdraw()  # hide window
    if save:
        fileName = tkinter.filedialog.asksaveasfile(
            parent=tkTop, defaultextension=".sv", filetypes=[("Save", "*.sv")]
        ).name
    else:
        fileName = tkinter.filedialog.askopenfilename(
            parent=tkTop, defaultextension=".sv", filetypes=[("Save", "*.sv")]
        )
    tkTop.destroy()
    PATH = fileName


def lighting(image, sv, tf):

    x, y = image.get_rect().size
    n = int(y - y / 3 * 2)

    k = 0
    if tf:
        k += sv
        for i in range(n):
            for j in range(y):
                r, g, b = image.get_at((j, i))[:3]
                image.set_at(
                    (j, i), (int(r + k // 50), int(g + k // 50), int(b + k // 50))
                )
            if k < 1:
                break
            else:
                k -= 1


def main(
    screen,
    playerConfig=[[Settings.WIDTH // 2, Settings.HEIGHT // 2], [2, 8]],
    seed=GenerationSettings.SEED,
):

    entitiesSprites = pygame.sprite.Group()
    entities = []

    player = Player.Player(playerConfig[0][0], playerConfig[0][1], screen)
    entities.append(player)
    player.inventory = Inventory.Inventory.Inventory(player)

    heightMap = HeightMap()
    heightMap.Generate(seed)
    startChunk = Generation.Chunk.Chunk(
        [playerConfig[1][0], playerConfig[1][1]], player, screen
    )
    startChunk.Generate(screen, heightMap)
    entitiesSprites.add(startChunk.listBlocks)
    entitiesSprites.add(player)

    player.chunk = startChunk
    visibleChunks = [startChunk]

    timer = pygame.time.Clock()
    tick = 0
    sv = 0
    toofar = True
    if True:
        while True:
            if 0 <= tick < 300:
                sv += 1
            elif 300 <= tick < 600:
                sv -= 1
            screen.fill((0, 0, 0))
            playerPos = player.Position

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Changes.FixChange.SaveChanges(
                        PATH, playerPos, player.inventory, seed, player.chunk
                    )
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 3 or event.button == 1:
                        mouseClick = pygame.mouse.get_pos()
                        for cell in player.inventory.Cells:
                            if cell.button.rect.collidepoint(mouseClick):
                                cell.button.Function()

                        distX, distY = (
                            mouseClick[0] - Settings.HALF_WIDTH,
                            mouseClick[1] - Settings.HALF_HEIGHT,
                        )
                        distX = distX // GenerationSettings.SIZEBLOCK
                        distY = distY // GenerationSettings.SIZEBLOCK

                        playerBlockX = playerPos[0] // GenerationSettings.SIZEBLOCK
                        playerBlockY = playerPos[1] // GenerationSettings.SIZEBLOCK
                        blockCoords = [
                            (playerBlockX + distX) * GenerationSettings.SIZEBLOCK,
                            (playerBlockY + distY) * GenerationSettings.SIZEBLOCK,
                        ]

                        for chunk in visibleChunks:

                            if chunk.CheckCoordsInside(blockCoords):
                                if event.button == 3 and player.chooseCell:
                                    if player.chooseCell.idIn != 0:
                                        block = Block(
                                            blockCoords[0],
                                            blockCoords[1],
                                            player.chooseCell.idIn,
                                            screen,
                                        )
                                        player.chooseCell.DeleteItem()
                                        if block not in chunk.listBlocks:
                                            chunk.listBlocks.append(block)
                                            entitiesSprites.add(block)
                                            change = Changes.Change.Change(
                                                "create", block
                                            )
                                            Changes.FixChange.Append(change)

                                else:
                                    for block in chunk.listBlocks:

                                        if (
                                            block.Position[0] == blockCoords[0]
                                            and block.Position[1] == blockCoords[1]
                                        ):
                                            item = block.GenerateItem(chunk)
                                            chunk.listBlocks.remove(block)
                                            entitiesSprites.remove(block)
                                            entitiesSprites.add(item)

                                            chunk.entity.append(item)
                                            entities.append(item)

                                            change = Changes.Change.Change(
                                                "break", block
                                            )
                                            Changes.FixChange.Append(change)

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

            for entity in entities:
                entity.Update()

            chunk = player.chunk.GenerateNext(heightMap)

            if chunk and chunk not in visibleChunks:
                visibleChunks.append(chunk)

                entitiesSprites.add(chunk.listBlocks)

            xOffset = Settings.HALF_WIDTH - playerPos[0]
            yOffset = Settings.HALF_HEIGHT - playerPos[1]

            for chunk in visibleChunks:

                if chunk.CheckCoordsInside(playerPos):
                    player.chunk = chunk
                if (
                    playerPos[0]
                    > (chunk.positionStart[0] + GenerationSettings.BLOCKS_IN_CHUNK * 2)
                    * GenerationSettings.SIZEBLOCK
                ):
                    entitiesSprites.remove(chunk.listBlocks)
                    entitiesSprites.remove(chunk.entity)
                    visibleChunks.remove(chunk)
                    chunk.DestroyChunk()

                elif (
                    playerPos[0]
                    < (chunk.positionStart[0] - GenerationSettings.BLOCKS_IN_CHUNK * 2)
                    * GenerationSettings.SIZEBLOCK
                ):
                    entitiesSprites.remove(chunk.listBlocks)
                    entitiesSprites.remove(chunk.entity)
                    visibleChunks.remove(chunk)
                    chunk.DestroyChunk()

            item = player.TryItemAppend()
            if item:
                player.inventory.AddItem(item)
                item.chunk.entity.remove(item)
                entitiesSprites.remove(item)
                item = None

            for entity in entitiesSprites:
                if tick % Settings.FPS:
                    lighting(entity._Image, sv, toofar)
                screen.blit(
                    entity._Image,
                    (entity.Position[0] + xOffset, entity.Position[1] + yOffset),
                )

            for cell in player.inventory.Cells:
                cell.Draw(screen)

            timer.tick(Settings.FPS)
            pygame.display.flip()


def SaveNewWorld(screen):
    Path(True)
    main(screen)


def LoadWorld(screen):
    Path()
    Changes.LoadSave.LoadWorld(PATH, main, screen)


if __name__ == "__main__":
    pygame.init()
    load = True
    screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
    running = True
    NewWorld = Button.Button(
        [Settings.WIDTH // 2, Settings.HEIGHT // 2],
        (300, 100),
        "Create new world",
        SaveNewWorld,
    )
    OpenWorld = Button.Button(
        [Settings.WIDTH // 2, Settings.HEIGHT // 2 + 150],
        (300, 100),
        "Open world",
        LoadWorld,
    )
    buttons = [NewWorld, OpenWorld]
    timer = pygame.time.Clock()
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    position = pygame.mouse.get_pos()
                    for button in buttons:
                        if button.rect.collidepoint(position):
                            button.Function(screen)
                            running = False
                            break

        for b in buttons:
            b.draw(screen)

        timer.tick(60)
        pygame.display.flip()
