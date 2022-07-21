from settings import *
from effects import Explosion, Smoke


class Ordnance(pygame.sprite.Sprite):
    def __init__(self, carrier, pylon_index):
        super().__init__()
        self.carrier = carrier
        self.pylon_index = pylon_index
        self.pos = self.carrier.pylons[self.pylon_index].pos_call()
        self.angle = self.carrier.angle
        self.size = 0.2
        self.speed = 2
        self.attached = True
        self.Ordnance_type = "bomb"
        self.stored = pygame.image.load('Assets/Ordnance/bomb.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.stored, self.angle, self.size)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

        ordnance_group.add(self)

    def update_images(self):
        self.image = pygame.transform.rotozoom(self.stored, self.angle, self.size)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def check_out_of_bounds(self, f=None):
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            if f:
                f()
            self.kill()

    def deploy(self):
        self.attached = False


class Bomb(Ordnance):
    def __init__(self, carrier, pylon_index):
        super().__init__(carrier, pylon_index)
        self.stored = pygame.image.load('Assets/Ordnance/bomb.png').convert_alpha()
        self.size = 0.2
        self.drop_speed = 0.0005
        self.detonation_height = 0.14

    def update(self):
        if self.attached:
            self.pos = pygame.math.Vector2(self.carrier.pylons[self.pylon_index].pos_call())
            self.angle = self.carrier.angle
        else:
            v = pygame.math.Vector2(self.speed / 1.5, 0).rotate(self.angle)
            self.pos.x += v[0]
            self.pos.y -= v[1]

            self.size -= self.drop_speed
            if self.size <= self.detonation_height:
                Explosion.add_explosion(self.rect.center)
                self.kill()

        self.update_images()


class Sidewinder(Ordnance):
    def __init__(self, carrier, pylon_index, target_group):
        super().__init__(carrier, pylon_index)
        self.stored = pygame.transform.rotozoom(
            pygame.image.load('Assets/Vehicles/ManAA/missile.png').convert_alpha(), 0, 0.1)
        self.size = 0.5
        self.Ordnance_type = "aa-missile"
        self.burner = 90
        self.speed = 4
        self.target_group = target_group
        self.target = None

    def predicted_los(self, target, r=0):
        if target:
            t = dis_to(self.rect.center,
                       self.predicted_los(target, r=r + 1) if r <= 2 else target.rect.center) / self.speed
            return target.rect.centerx + (target.v[0] * int(t)), target.rect.centery + (
                    -target.v[1] * int(t))
        else:
            return 0

    def deploy(self):
        self.attached = False
        self.target = closest_target(self, self.target_group, max_range=650, angle_limit=30, exclude=self.carrier)
        if self.target:
            try:
                self.target.threats.append(self)

            except AttributeError:
                pass
            except ValueError:
                pass

    def remove_threat(self):
        if self.target:
            try:
                self.target.threats.remove(self)
            except Exception as e:
                print(self.target)
                print(e)

    def check_for_hit(self):
        for overlap in overlaps_with(self, self.target_group.sprites()):
            if overlap is not self.carrier:
                self.remove_threat()
                overlap.health = 0
                self.kill()

    def update(self):
        if self.attached:
            self.pos = pygame.math.Vector2(self.carrier.pylons[self.pylon_index].pos_call())
            self.angle = self.carrier.angle
        else:
            self.check_for_hit()
            self.check_out_of_bounds(f=self.remove_threat)
            if self.target:
                face_to(self, self.predicted_los(self.target), self.speed)
                if gimbal_limit(self, dir_to(self.rect.center, self.target.rect.center), 70):
                    self.target = None

            # Slow down the missile
            self.burner -= 1
            if self.burner <= 0:
                self.speed *= 0.993
                if self.speed <= 0.5:
                    self.remove_threat()
                    self.kill()
            else:
                Smoke.add_smoke(self.rect.center, spreadx=(-0.2, 0.2), spready=(-0.2, 0.2), size=0.1)

            # Move the missile
            v = pygame.math.Vector2((self.speed, 0)).rotate(self.angle)
            self.pos[0] += v[0]
            self.pos[1] -= v[1]

        self.update_images()


ordnance_group = pygame.sprite.Group()
