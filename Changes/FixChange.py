Changes = []


def Append(NewChange):
    if NewChange in Changes:
        return

    for change in Changes:
        if change.block == NewChange.block:
            return

    Changes.append(NewChange)


def GetBlockChanged():
    return [i.block for i in Changes]


def SaveChanges(Path, playerPos, Inventory, Seed, chunk):

    with open(Path, "w") as Save:
        for change in Changes:
            position = change.block.Position
            Save.write(
                f"{change.type}/{position[0]}, {position[1]}/{change.block._id};"
            )

        Save.write(f"\n")
        Save.write(f"{playerPos[0]},{playerPos[1]}\n")
        Save.write(f"{chunk.positionStart[0]},{chunk.positionStart[1]}\n")
        Save.write(f"{Seed}\n")
        for index, cell in enumerate(Inventory.Cells):
            indexCell, idIn, count = index, cell.idIn, cell.countItem
            Save.write(f"{indexCell}:{idIn}:{count};")

        Save.close()


def GetChanges():
    return Changes
