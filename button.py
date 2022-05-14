import pygame

import Vehicles
from settings import *
import placer


class Button(pygame.sprite.Sprite):
    def __init__(self, pos, obj):
        super().__init__()
        self.image = pygame.Surface((100, 100))  # Create Surface

        # Create preview image and blit it
        i = obj.preview
        i_r = i.get_rect(center=(self.image.get_width() / 2, self.image.get_height() / 2))
        self.image.blit(i, i_r)

        # Create rect and mask
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

        # Save data to pass onto blueprint
        self.obj = obj

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            placer.in_hand = True
            placer.blueprint_group.add(placer.blueprint(self.obj))

    def update(self):
        pass


buttons = pygame.sprite.Group()
buttons.add(Button((200, 500), Vehicles.Vads))
buttons.add(Button((200, 600), Vehicles.Grad))
