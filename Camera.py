import pygame
import Settings
class Camera():
    def __init__(self, width, height):
        self.camera_func = camera_configure
        self.state = pygame.Rect(0, 0, width, height)

    def Apply(self, target):
        return target.rect.move(self.state.topleft)

    def Update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+Settings.WIDTH / 2, -t+Settings.HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width-Settings.WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height-Settings.HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)