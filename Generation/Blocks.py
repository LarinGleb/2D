import pygame

import sys

sys.path.append("../Sprites")


GRASS = pygame.image.load("Sprites/Grass.jpg")
ROOTS = pygame.image.load("Sprites/ROOTS.jpg")
EARTH = pygame.image.load("Sprites/EARTH.jpg")
STONE = pygame.image.load("Sprites/STONE.jpg")

idBlock = {1: GRASS, 2: ROOTS, 3: EARTH, 4: STONE}
