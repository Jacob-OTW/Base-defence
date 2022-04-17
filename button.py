import pygame

import hand
from settings import *
from hand import blueprint_group, blueprint, in_hand


class island(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        self.rect = self.image.get_rect(left=0, bottom=SCREEN_HEIGHT)
        self.mask = pygame.mask.from_surface(self.image)

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            hand.in_hand = True
            blueprint_group.add(blueprint('Assets/plane.png', 0.1))

    def update(self):
        pass


x_group = pygame.sprite.Group(island())
