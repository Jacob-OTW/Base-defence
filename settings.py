import pygame
import math
import time
import random
import sys

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()

score_font = pygame.font.SysFont("arial", 32, pygame.font.Font.bold)


def dir_to(mp, tp):
    dx = tp[0] - mp[0]
    dy = tp[1] - mp[1]
    rads = math.atan2(-dy, dx)
    rads %= 2 * math.pi
    return math.degrees(rads)


def relative_mouse(m=None):
    if m is None:
        m = pygame.mouse.get_pos()
    x = m[0] / (display.get_width() / screen.get_width())
    y = m[1] / (display.get_width() * SCREEN_HEIGHT/SCREEN_WIDTH / screen.get_height())
    return x, y


def round_to_360(x):
    r = math.degrees(math.asin(math.sin(math.radians(x))))
    if r > 0:
        return r
    return abs(r - 180)


def dis_to(mp, tp):
    return math.hypot(mp[0] - tp[0], mp[1] - tp[1])


def face_to(self, ang, turn_limit):
    angle = dir_to(self.rect.center, ang)
    self.angle += math.sin(math.radians(angle - self.angle)) * turn_limit


def gimbal_limit(self, angle: int | float, limit: int | float) -> bool:
    """
    Return a bool if the target of the missile is outside its turn radius.
    param self: an object that has an angle attribute.
    param angle: an angle as an integer or float to where the missile is meant to fly.
    param limit: the max. difference between where the missile is pointed and where it is meant to fly.
    return: bool if the gimbal limit was reached.
    """
    return abs(((self.angle - angle) + 180) % 360 - 180) > limit


def closest_target(self, sprites: list, max_range=250, angle_limit=0, exclude=None):
    compare = {max_range: None}
    for sprite in sprites:
        if sprite is not exclude:
            if angle_limit == 0:
                compare[dis_to(self.rect.center, sprite.rect.center)] = sprite
            else:
                if not gimbal_limit(self, dir_to(self.rect.center, sprite.rect.center), angle_limit):
                    compare[dis_to(self.rect.center, sprite.rect.center)] = sprite

    m = min(compare.keys())
    return compare[m]


def overlaps_with(self, group: pygame.sprite.Group) -> list:
    """
    The listed passed into the filter call checks rect collisions, then, only the objects
    that are also mask colliding will be keep, the final result will be returned
    """
    return list(filter(lambda obj: self.mask.overlap(obj.mask,
                                                     (obj.rect.x - self.rect.x, obj.rect.y - self.rect.y)),
                       pygame.sprite.spritecollide(self, group, False)))
