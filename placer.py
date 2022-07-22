from settings import *
from Vehicles import vehicle_group
from island import island


def fill(surface, color):
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))


class Blueprint(pygame.sprite.Sprite):
    def __init__(self, obj):
        super().__init__()
        self.obj = obj
        self.image = pygame.Surface.copy(obj.idle)
        self.image.set_alpha(75)
        fill(self.image, pygame.Color(10, 40, 250))
        self.rect = self.image.get_rect(center=pygame.mouse.get_pos())
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.center = relative_mouse()

    def place(self):
        global in_hand
        if self.mask.overlap(island.mask, (island.mask_rect.x - self.rect.x, island.mask_rect.y - self.rect.y)):
            vehicle_group.add(self.obj(self.rect.center))
            in_hand = False
            self.kill()


blueprint_group = pygame.sprite.GroupSingle()
in_hand = False
