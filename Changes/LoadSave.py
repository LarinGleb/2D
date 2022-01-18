from Changes import Change
from Generation import Block
from Changes import FixChange

import sys
sys.path.append("..")

def LoadWorld(savePath, GameFunc, screen):
    changes = []
    with open(savePath, "r") as Save:
        blocksChanged = Save.readline()
        if blocksChanged:
            blocksChanged = blocksChanged.split(";")
            blocksChanged = blocksChanged[:len(blocksChanged)-1]
            for c in blocksChanged:
                typeChange, coords, idBlock = c.split('/')
                coords = list(map(int, coords.split(',')))
                block = Block.Block(coords[0], coords[1], int(idBlock), screen)
                change = Change.Change(typeChange, block)
                changes.append(change)
        
        playerPos = list(map(int, Save.readline().split(',')))
        playerChunk = list(map(int, Save.readline().split(',')))
        seed = int(Save.readline())

    configPlayer = [playerPos, playerChunk]
    FixChange.Changes = changes
    GameFunc(screen, configPlayer, seed)
            