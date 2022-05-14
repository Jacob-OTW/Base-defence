import random

from settings import *
from planes import plane_group


class Grad(pygame.sprite.Sprite):
    class missile(pygame.sprite.Sprite):
        def __init__(self, pos):
            super().__init__()
            self.image = pygame.image.load('Assets/bullet.png').convert_alpha()
            self.rect = self.image.get_rect(center=pos)

        def update(self):
            self.rect.x += 1

    preview = pygame.image.load('Assets/Vehicles/Grad/preview.png').convert_alpha()
    idle = pygame.transform.rotozoom(pygame.image.load('Assets/Vehicles/Grad/idle.png').convert_alpha(), 0, 0.1)

    def __init__(self, pos):
        super().__init__()
        self.image = Grad.idle
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.a = Grad.missile(self.rect.center)
        vehicle_projectile_group.add(self.a)

    def update(self):
        pass


class Vads(pygame.sprite.Sprite):
    class Vads_bullet(pygame.sprite.Sprite):
        def __init__(self, pos, angle):
            super().__init__()
            angle += random.uniform(-5, 5)
            self.stored = pygame.image.load('Assets/bullet.png').convert_alpha()
            self.position = pygame.math.Vector2(pos)
            self.image = pygame.transform.rotozoom(self.stored, angle, 0.1)
            self.rect = self.image.get_rect(center=self.position)
            self.v = pygame.math.Vector2((5, 0)).rotate(angle)

        def update(self):
            self.position[0] += self.v[0]
            self.position[1] -= self.v[1]
            self.rect.center = self.position

            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
                self.kill()

    preview = pygame.image.load('Assets/Vehicles/Vads/preview.png').convert_alpha()
    idle = pygame.transform.rotozoom(pygame.image.load('Assets/Vehicles/Vads/idle.png').convert_alpha(), 0, 0.1)

    def __init__(self, pos):
        super().__init__()
        self.image = Vads.idle
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.target = None

    def predicted_los(self, target, r=0):
        if target:
            t = dis_to(self.rect.center, self.predicted_los(target, r=r + 1) if r <= 2 else target.rect.center) / 5
            return target.rect.centerx + (target.v[0] * int(t)), target.rect.centery + (
                    -target.v[1] * int(t))
        else:
            return 0

    def update(self):
        if plane_group.sprites():
            self.target = plane_group.sprites()[0]
        vehicle_projectile_group.add(self.Vads_bullet(self.rect.center,
                                                      dir_to(
                                                          self.rect.center, self.predicted_los(self.target))
                                                      )
                                     )


vehicle_group = pygame.sprite.Group()
vehicle_projectile_group = pygame.sprite.Group()
