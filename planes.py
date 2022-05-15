import random
import pygame
from settings import *


class Plane(pygame.sprite.Sprite):
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

    def rotate_img(self):
        self.image = pygame.transform.rotozoom(self.stored, self.angle, self.size)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def face_to(self, ang):
        self.angle = dir_to(self.rect.center, ang)

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


class F16(Plane):
    @classmethod
    def spawn_F16(cls):
        plane_group.add(F16(pos=(0, random.randint(50, SCREEN_HEIGHT - 50)), angle=0))

    def update(self):
        self.move(2)
        self.rotate_img()
        self.check_health()


plane_group = pygame.sprite.Group(Plane())
