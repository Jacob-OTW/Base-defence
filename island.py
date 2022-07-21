import pygame
from settings import *


class land(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/island.png').convert_alpha()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.mask_img = pygame.transform.rotozoom(pygame.image.load('Assets/island.png').convert_alpha(), 0, 0.75)
        self.mask_rect = self.mask_img.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.mask_img)

    def update(self):
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


land_group = pygame.sprite.Group(land())
