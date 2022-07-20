from settings import *
from planes import plane_group


class Grad(pygame.sprite.Sprite):
    __slots__ = ('image', 'rect')

    class Missile(pygame.sprite.Sprite):
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
        self.a = Grad.Missile(self.rect.center)
        vehicle_projectile_group.add(self.a)

    def update(self):
        pass


class Vads(pygame.sprite.Sprite):
    __slots__ = ('image', 'rect', 'mask', 'target')

    class VadsBullet(pygame.sprite.Sprite):
        __slots__ = ('stored', 'position', 'image', 'rect', 'mask', 'v')

        def __init__(self, pos, angle):
            super().__init__()
            angle += random.uniform(-5, 5)
            self.stored = pygame.image.load('Assets/bullet.png').convert_alpha()
            self.position = pygame.math.Vector2(pos)
            self.image = pygame.transform.rotozoom(self.stored, angle, 0.1)
            self.rect = self.image.get_rect(center=self.position)
            self.mask = pygame.mask.from_surface(self.image)
            self.v = pygame.math.Vector2((5, 0)).rotate(angle)

        def update(self):
            self.position[0] += self.v[0]
            self.position[1] -= self.v[1]
            self.rect.center = self.position

            col = pygame.sprite.spritecollide(self, plane_group, False)
            if col:
                if self.mask.overlap(col[0].mask,
                                     (col[0].rect.x - self.rect.x, col[0].rect.y - self.rect.y)):
                    col[0].health -= 1
                    self.kill()

            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH \
                    or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
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

    def shoot(self):
        if self.target:
            vehicle_projectile_group.add(
                self.VadsBullet(self.rect.center, dir_to(self.rect.center, self.predicted_los(self.target))))

    def update(self):
        self.target = closest_target(self, plane_group.sprites(), max_range=250)
        self.shoot()


class ManAA(pygame.sprite.Sprite):
    class ManAAMissile(pygame.sprite.Sprite):
        def __init__(self, pos, target):
            super().__init__()
            self.pos = pygame.math.Vector2(pos)
            self.stored = pygame.transform.rotozoom(
                pygame.image.load('Assets/Vehicles/ManAA/missile.png').convert_alpha(),
                0, 0.1)
            self.image = pygame.transform.rotate(self.stored, 0)
            self.rect = self.image.get_rect(center=self.pos)
            self.mask = pygame.mask.from_surface(self.image)

            self.target = target
            self.angle = dir_to(self.rect.center, self.target.rect.center)

            self.speed = 2.5

            self.lifespan = 500

        def predicted_los(self, target, r=0):
            if target:
                t = dis_to(self.rect.center, self.predicted_los(target, r=r + 1) if r <= 2 else target.rect.center) / 5
                return target.rect.centerx + (target.v[0] * int(t)), target.rect.centery + (
                        -target.v[1] * int(t))
            else:
                return 0

        def update(self) -> None:
            if self.target and self.mask.overlap(self.target.mask,
                                                 (self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y)):
                self.target.kill()
                self.kill()

            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
                self.kill()

            if self.target:
                face_to(self, self.predicted_los(self.target), 2.5)

            v = pygame.math.Vector2((self.speed, 0)).rotate(self.angle)
            self.pos[0] += v[0]
            self.pos[1] -= v[1]

            # Update
            self.image = pygame.transform.rotate(self.stored, self.angle)
            self.rect = self.image.get_rect(center=self.pos)
            self.mask = pygame.mask.from_surface(self.image)

    preview = pygame.image.load('Assets/Vehicles/ManAA/preview.png').convert_alpha()
    idle = pygame.transform.rotozoom(pygame.image.load('Assets/Vehicles/ManAA/idle.png').convert_alpha(), 0, 0.1)

    def __init__(self, pos):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.stored = ManAA.idle
        self.image = pygame.transform.rotate(self.stored, 0)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.target = None

        self.fire_timer = 0

    def shoot(self):
        if self.target:
            vehicle_projectile_group.add(
                self.ManAAMissile(self.pos, self.target)
            )

    def update(self):
        self.target = closest_target(self, plane_group.sprites(), max_range=350)
        self.fire_timer += 1
        if self.target and self.fire_timer % 300 == 0:
            self.shoot()


vehicle_group = pygame.sprite.Group()
vehicle_projectile_group = pygame.sprite.Group()
