import pygame
from settings import *


class objX(pygame.sprite.Sprite):
    def __init__(self, img_path, img_size=1):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(img_path).convert_alpha(), 0, img_size)
        self.rect = self.image.get_rect(center=pygame.mouse.get_pos())
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass


object_group = pygame.sprite.Group()
