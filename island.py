import pygame
from settings import *


class land(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/island.png').convert_alpha()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.draw_mask_attach()

    def draw_mask_attach(self):  # Draws the hitbox at the bottom of player for debugging
        olist = self.mask.outline()
        img = pygame.Surface([640, 480], pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.lines(img, (200, 150, 150), True, olist)
        screen.blit(img, (self.rect.x, self.rect.y))


land_group = pygame.sprite.Group()
island = land()
land_group.add(island)
