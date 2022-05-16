import pygame

from settings import *


class ShowElement(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('Assets/bullet.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)


class Plane(pygame.sprite.Sprite):
    element_group = pygame.sprite.Group()

    def __init__(self, pos=(0, 0), angle=0, img_path='Assets/Planes/F16.png'):
        super().__init__()
        self.position = pygame.math.Vector2(pos)
        self.angle = angle
        self.v = pygame.math.Vector2((0, 0))
        self.health = 100
        self.stored = pygame.image.load(img_path).convert_alpha()
        self.size = 0.3
        self.image = pygame.transform.rotozoom(self.stored, 0, self.size)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

        # Path
        self.path = []
        self.waypoint = None
        self.create_path()
        """
        for point in self.path:
            Plane.element_group.add(ShowElement(point))
        """

    def rotate_img(self):
        self.image = pygame.transform.rotozoom(self.stored, self.angle, self.size)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def face_to(self, ang, speed=5):
        angle = dir_to(self.rect.center, ang)
        self.angle += math.sin(math.radians(angle - self.angle)) * speed

    def move(self, amount):
        self.v = pygame.math.Vector2((amount, 0)).rotate(self.angle)
        self.position[0] += self.v[0]
        self.position[1] -= self.v[1]
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def check_health(self):
        if self.health <= 0:
            self.kill()

    def update(self):
        self.face_to(pygame.mouse.get_pos())
        self.move(2)
        self.rotate_img()

    def create_path(self):
        for i in range(int(round(SCREEN_WIDTH / 10))):
            self.path.append((self.rect.centerx + (SCREEN_WIDTH / 10) * i, self.rect.centery + random.uniform(-50, 50)))
            self.waypoint = self.path[0]

    def next_waypoint(self):
        self.waypoint = self.path[self.path.index(self.waypoint) + 1]


class F16(Plane):
    @classmethod
    def spawn_f16(cls):
        plane_group.add(F16(pos=(0, random.randint(50, SCREEN_HEIGHT - 50)), angle=0))

    def update(self):
        if self.rect.centerx > self.waypoint[0]:
            self.next_waypoint()
        self.face_to(self.waypoint, speed=1)
        self.move(2)
        self.rotate_img()
        self.check_health()


plane_group = pygame.sprite.Group(Plane(pos=(0, SCREEN_HEIGHT / 2)))
