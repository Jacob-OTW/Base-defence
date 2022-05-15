import pygame
import sys
import time
import math

import placer
from settings import *
from island import land_group
from button import buttons
from placer import blueprint_group
from Vehicles import vehicle_group, vehicle_projectile_group
from planes import plane_group, F16


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
    total_timer = 0
    last_time = time.time()
    while True:
        frame_time = time.time() - last_time
        last_time = time.time()
        # Events
        land_group.update()
        blueprint_group.update()
        vehicle_group.update()
        vehicle_projectile_group.update()
        plane_group.update()
        HandleKeys()

        # Timers
        total_timer += 1
        if total_timer % 60 == 0:
            F16.spawn_F16()

        # Visual
        screen.fill((1, 201, 250))
        land_group.draw(screen)
        buttons.draw(screen)
        blueprint_group.draw(screen)
        vehicle_projectile_group.draw(screen)
        vehicle_group.draw(screen)
        plane_group.draw(screen)

        text2 = score_font.render(f"{round(frame_time * 1000)}ms", True, (255, 255, 255))
        screen.blit(text2, (100, 150))

        # Refresh
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
