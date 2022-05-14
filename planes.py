import pygame
import math

from settings import *


class Plane(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), angle=0):
        super().__init__()
        self.launch()
        self.position = pygame.math.Vector2(pos)
        self.angle = angle
        self.v = pygame.math.Vector2((0, 0))
        self.stored = pygame.image.load('Assets/Planes/F16.png').convert_alpha()
        self.size = 0.3
        self.image = pygame.transform.rotozoom(self.stored, 0, self.size)
        self.rect = self.image.get_rect(center=self.position)

    def launch(self):
        print('launch')

    def rotate_img(self):
        self.image = pygame.transform.rotozoom(self.stored, self.angle, self.size)
        self.rect = self.image.get_rect(center=self.position)

    def face_to(self, ang):
        self.angle = dir_to(self.rect.center, ang)

    def move(self, amount):
        self.v = pygame.math.Vector2((amount, 0)).rotate(self.angle)
        self.position[0] += self.v[0]
        self.position[1] -= self.v[1]

    def update(self):
        self.face_to(pygame.mouse.get_pos())
        self.move(2)
        self.rotate_img()


class F16(Plane):
    def update(self):
        self.move(2)
        self.rotate_img()


plane_group = pygame.sprite.GroupSingle(F16(pos=(0, 500), angle=0))
