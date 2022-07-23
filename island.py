import pygame

from settings import *


class land(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/island.png').convert_alpha()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


class Runway(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.angle = angle
        self.size = 0.65
        self.stored = pygame.image.load('Assets/Runway.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.stored, self.angle, self.size)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass


island = land()
land_group = pygame.sprite.Group(island)
runway_group = pygame.sprite.Group(Runway((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2), 90))
