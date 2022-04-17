import pygame
import sys
import time
import math

import placer
from settings import *
from island import land_group
from button import buttons
from placer import blueprint_group
from Vehicles import object_group


def HandleKeys():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not placer.in_hand:
                for s in buttons.sprites():
                    s.check_click(event.pos)
            else:
                blueprint_group.sprites()[0].place()


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
        buttons.draw(screen)
        blueprint_group.draw(screen)
        object_group.draw(screen)

        text2 = score_font.render(f"{round(frame_time * 1000)}ms", True, (255, 255, 255))
        screen.blit(text2, (100, 150))

        # Refresh
        pygame.display.flip()
        clock.tick(60)


main()
