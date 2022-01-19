from . import Cell
import pygame

COUNT_CELL = 10
CELL_SIZE = 64


class Inventory:
    def __init__(self, player):
        self.Cells = []
        self.player = player
        for i in range(0, COUNT_CELL):
            cell = Cell.Cell([(i + 1) * CELL_SIZE, CELL_SIZE // 2], player)
            self.Cells.append(cell)

    def AddItem(self, item):
        for cell in self.Cells:
            if item.id == cell.idIn:
                if not cell.busy:
                    cell.UpdateCount()
                    break
            elif cell.idIn == 0:
                cell.AddItem(item)
                break
