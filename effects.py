from settings import *


class Explosion(pygame.sprite.Sprite):
    @classmethod
    def add_explosion(cls, pos):
        explosion_group.add(Explosion(pos))

    def __init__(self, pos):
        super().__init__()
        self.stored = pygame.transform.rotozoom(pygame.image.load('Assets/effects/explosion_air.png').convert_alpha(), 0, 0.8)
        self.size = 0.1
        self.pos = pos
        self.image = pygame.transform.rotozoom(self.stored, 0, self.size)
        self.rect = self.image.get_rect(midbottom=pos)
        self.opacity = 255

    def update(self):
        self.image = pygame.transform.rotozoom(self.stored, 0, self.size)
        self.rect = self.image.get_rect(center=self.pos)
        if self.size <= 1:
            self.size += 0.1
        else:
            self.opacity -= 4.5
            self.image.set_alpha(self.opacity)
            if self.opacity <= 0:
                self.kill()


class Smoke(pygame.sprite.Sprite):
    @classmethod
    def add_smoke(cls, pos, m_vec=None, spreadx=(-1, 1), spready=(-1, 1), size=0.2, opacity=255):
        smoke_group.add(Smoke(pos, m_vec=m_vec, spreadx=spreadx, spready=spready, size=size, opacity=opacity))

    def __init__(self, pos, m_vec=None, spreadx=(-1, 1), spready=(-1, 1), size=0.2, opacity=255):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load('Assets/effects/smoke.png').convert_alpha(), 0, size)
        self.pos = pygame.math.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)
        self.opacity = opacity
        self.fall_speed = 0.3
        self.vec = pygame.math.Vector2(random.uniform(spreadx[0], spreadx[1]), random.uniform(spready[0], spready[1]))
        self.m_vec = m_vec

    def update(self):
        self.pos[1] += self.fall_speed
        self.pos += self.vec
        if self.m_vec:
            self.pos[0] += self.m_vec[0]
            self.pos[1] -= self.m_vec[1]
        self.rect.center = self.pos
        self.image.set_alpha(self.opacity)
        self.opacity -= 5
        if self.opacity <= 0:
            self.kill()


class Flare(pygame.sprite.Sprite):
    @classmethod
    def add_flare(cls, pos, threats):
        flare_group.add(Flare(pos, threats))

    def __init__(self, pos, carrier_threats):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.size = 0.5
        self.v = pygame.math.Vector2(random.uniform(-0.15, 0.15), random.uniform(-0.15, 0.15))
        self.threats = []
        self.stored = pygame.image.load('Assets/effects/flares.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.stored, 0, self.size)
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

        for threat in carrier_threats:
            if random.uniform(0, 1) < threat.trash_chance:
                try:
                    threat.remove_threat()
                    self.threats.append(threat)
                    threat.target = self
                except AttributeError:
                    pass
                except ValueError:
                    pass

    def update(self):
        if random.randint(0, 10) == 0:
            Smoke.add_smoke(self.rect.center, size=0.1)

        self.size *= 0.99
        if self.size < 0.1:
            self.kill()
        self.image = pygame.transform.rotozoom(self.stored, 0, self.size)

        self.pos += self.v
        self.rect.center = self.pos


explosion_group = pygame.sprite.Group()
smoke_group = pygame.sprite.Group()
flare_group = pygame.sprite.Group()
