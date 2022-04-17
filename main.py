import pygame
import sys
import time
import math

import hand
from settings import *
from island import land_group
from button import x_group
from hand import blueprint_group
from ObjectX import object_group


def HandleKeys():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not hand.in_hand:
                for s in x_group.sprites():
                    s.check_click(event.pos)
            else:
                blueprint_group.sprites()[0].place()


class Island(pygame.sprite.Sprite):
    def __int__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/island.png').convert_alpha()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    def update(self):
        pass


island_group = pygame.sprite.GroupSingle(Island())


def main():
    last_time = time.time()
    while True:
        frame_time = time.time() - last_time
        last_time = time.time()
        # Events
        land_group.update()
        blueprint_group.update()
        HandleKeys()

        # Visual
        screen.fill((1, 201, 250))
        land_group.draw(screen)
        x_group.draw(screen)
        blueprint_group.draw(screen)
        object_group.draw(screen)

        text2 = score_font.render(f"{round(frame_time * 1000)}ms {hand.in_hand}", True, (255, 255, 255))
        screen.blit(text2, (100, 150))

        # Refresh
        pygame.display.flip()
        clock.tick(60)


main()
