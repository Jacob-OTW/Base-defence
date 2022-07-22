import pygame.transform

import placer
from settings import *
from island import land_group
from button import buttons
from placer import blueprint_group
from Vehicles import vehicle_group, vehicle_projectile_group
from planes import plane_group, aim_cross_group, F16, Plane
from effects import smoke_group, flare_group, explosion_group
from Ordnance import ordnance_group


def handle_keys():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            print(event.w, event.h)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                F16.spawn_f16()
            elif event.key == pygame.K_w:
                plane_group.sprites()[0].flare()
            elif event.key == pygame.K_e:
                for pylon in plane_group.sprites()[0].pylons:
                    if pylon.item is not None:
                        pylon.fire()
                        break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not placer.in_hand:
                for s in buttons.sprites():
                    s.check_click(relative_mouse(event.pos))
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
        smoke_group.update()
        flare_group.update()
        ordnance_group.update()
        aim_cross_group.update()
        explosion_group.update()
        handle_keys()

        # Timers
        total_timer += 1
        if total_timer % 500 == 0:
            pass
            # F16.spawn_f16()

        # Visual
        screen.fill((1, 201, 250))
        land_group.draw(screen)
        buttons.draw(screen)
        blueprint_group.draw(screen)
        vehicle_projectile_group.draw(screen)
        vehicle_group.draw(screen)
        explosion_group.draw(screen)
        ordnance_group.draw(screen)
        plane_group.draw(screen)
        flare_group.draw(screen)
        smoke_group.draw(screen)
        aim_cross_group.draw(screen)
        Plane.element_group.draw(screen)

        text2 = score_font.render(f"{round(frame_time * 1000)}ms", True, (255, 255, 255))
        screen.blit(text2, (100, 150))

        display.blit(
            pygame.transform.scale(screen, (display.get_width(), display.get_width() * SCREEN_HEIGHT / SCREEN_WIDTH))
            , (0, 0))

        # Refresh
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
