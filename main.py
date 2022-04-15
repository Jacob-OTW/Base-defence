import pygame
import sys
import time
import math

from settings import *

from Island import island_group


def HandleKeys():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pass


def main():
    last_time = time.time()
    while True:
        frame_time = time.time() - last_time
        last_time = time.time()
        # Events
        island_group.update()
        HandleKeys()

        # Visual
        screen.fill((1, 201, 250))
        island_group.draw(screen)

        text2 = score_font.render(f"{round(frame_time * 1000)}ms", True, (255, 255, 255))
        screen.blit(text2, (100, 150))

        # Refresh
        pygame.display.flip()
        clock.tick(60)


main()
