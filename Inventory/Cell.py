
import pygame
import sys
from . import Inventory

sys.path.append("..")
import Button
from Generation import Blocks


class Cell:
    def __init__(self, position, player):

        self.player = player
        self.position = position
        self.button = Button.Button(
            position,
            (Inventory.CELL_SIZE, Inventory.CELL_SIZE),
            "",
            self.ChooseBlock,
            14,
            [50, 50, 50],
        )
        self.StartState()
        pygame.font.init()
        self.font = pygame.font.SysFont("Times New Roman", 14)
        self.txtSurface = self.font.render('0', 1, [255, 255, 255])

    def StartState(self):
        self.idIn = 0
        self.maxCount = 0
        self.countItem = 0
        self.busy = False
        self.txt = '0'

    def UpdateText(self):
        self.txt = str(self.countItem)
        self.txtSurface = self.font.render(self.txt, 1, [255, 255, 255])

    def Draw(self, screen):
        
        self.button.draw(screen)

        if self.idIn > 0:
            sizePicture = Inventory.CELL_SIZE // 2
            screen.blit(
                pygame.transform.scale(
                    Blocks.idBlock[self.idIn], (sizePicture, sizePicture)
                ),
                (
                    self.position[0] - sizePicture // 2,
                    self.position[1] - sizePicture // 2,
                ),
            )
        pygame.draw.line(
            screen,
            (155, 155, 155),
            (Inventory.CELL_SIZE // 2, Inventory.CELL_SIZE),
            (
                Inventory.COUNT_CELL * Inventory.CELL_SIZE + Inventory.CELL_SIZE // 2,
                Inventory.CELL_SIZE,
            ),
            2,
        )
        pygame.draw.line(
            screen,
            (155, 155, 155),
            (Inventory.CELL_SIZE // 2, 0),
            (Inventory.CELL_SIZE // 2, Inventory.CELL_SIZE),
            2,
        )
        pygame.draw.line(
            screen,
            (155, 155, 155),
            (Inventory.COUNT_CELL * Inventory.CELL_SIZE + Inventory.CELL_SIZE // 2, 0),
            (
                Inventory.COUNT_CELL * Inventory.CELL_SIZE + Inventory.CELL_SIZE // 2,
                Inventory.CELL_SIZE,
            ),
            2,
        )

        screen.blit(self.txtSurface, self.position)

    def AddItem(self, item):
        self.countItem = 1
        self.idIn = item.id
        self.maxCount = item.maxCount
        self.UpdateText()

    def DeleteItem(self):
        self.countItem -= 1
        self.UpdateText()
        if self.countItem == 0:
            self.StartState()

    def UpdateCount(self):
        self.countItem += 1
        self.UpdateText()
        print(self.countItem)
        self.busy = self.countItem == self.maxCount
            

    def ChooseBlock(self):
        self.player.chooseCell = self
