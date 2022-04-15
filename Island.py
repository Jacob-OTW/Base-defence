import pygame
from settings import *


class Island(pygame.sprite.Sprite):
    def __int__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/island.png').convert_alpha()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def update(self):
        pass


island_group = pygame.sprite.GroupSingle(Island())
