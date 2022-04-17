import pygame
from settings import *


class island(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/island.png').convert_alpha()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass


land_group = pygame.sprite.Group()
land_group.add(island())
