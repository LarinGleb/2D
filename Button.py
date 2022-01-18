import pygame
import Settings
class Button:
    def __init__(self, position, size, text, func, fontsize = 24, background = Settings.GREEN):
        self.func = func
        self.size = size
        self.background = background
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect(center=position)

        self.font = pygame.font.SysFont("Times New Roman", fontsize)
        self.txt = text
        self.txtSurface = self.font.render(self.txt, 1, [0, 0, 0])
        self.txtRect = self.txtSurface.get_rect(center=[size[0] // 2, size[1] // 2])

    def draw(self, screen):
        self.surface.fill(self.background)
        self.surface.blit(self.txtSurface, self.txtRect)
        screen.blit(self.surface, self.rect)

    def Function(self, *args):
        self.func(*args)
