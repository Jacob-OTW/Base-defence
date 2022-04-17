import pygame
from settings import *
from ObjectX import object_group, objX
from island import island


def fill(surface, color):
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))


class blueprint(pygame.sprite.Sprite):
    def __init__(self, img_path, img_size=1):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(img_path).convert_alpha(), 0, img_size)
        self.image.set_alpha(75)
        fill(self.image, pygame.Color(10, 40, 250))
        self.rect = self.image.get_rect(center=pygame.mouse.get_pos())
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.draw_mask_attach()

    def place(self):
        global in_hand
        if self.mask.overlap_mask(island.mask, (island.rect.x - self.rect.x, island.rect.y - self.rect.y)):
            object_group.add(objX('Assets/plane.png', 0.1))
            in_hand = False
            self.kill()

    def draw_mask_attach(self):  # Draws the hitbox at the bottom of player for debugging
        olist = self.mask.outline()
        img = pygame.Surface([640, 480], pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.lines(img, (200, 150, 150), True, olist)
        screen.blit(img, (self.rect.x, self.rect.y))


blueprint_group = pygame.sprite.GroupSingle()
in_hand = False
