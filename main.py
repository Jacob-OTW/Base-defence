from settings import *
from island import land_group, runway_group
from button import buttons
from Vehicles import vehicle_group, vehicle_projectile_group, blueprint_group
from planes import plane_group, aim_cross_group, F16, element_group, player
from effects import smoke_group, flare_group, explosion_group
from Ordnance import ordnance_group
from GUI import gui_group, GUI
import Vehicles


def handle_keys():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            pass
            # print(event.w, event.h)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                F16.spawn_f16()
            elif event.key == pygame.K_w:
                plane_group.sprites()[0].flare()
            elif event.key == pygame.K_e:
                player.pylons.cur.data.fire()
            elif event.key == pygame.K_d:
                player.pylons.next()
            elif event.key == pygame.K_a:
                player.pylons.previous()
            elif event.key == pygame.K_f and player.landed:
                add_ui()
            elif event.key == pygame.K_DOWN and player.landed and player.guis:
                player.guis[-1].buttons.next()
            elif event.key == pygame.K_UP and player.landed and player.guis:
                player.guis[-1].buttons.previous()
            elif event.key == pygame.K_RETURN and player.landed and player.guis:
                player.guis[-1].buttons.cur.data.callback_f()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not Vehicles.in_hand:
                for s in buttons.sprites():
                    s.check_click(relative_mouse(event.pos))
            else:
                blueprint_group.sprites()[0].place()


def add_ui():
    def stick_to_plane(gui: GUI, *args):
        gui.set_rect(topleft=player.rect.bottomright)

    def add_to_output(button: GUI.GUI_Button, *args):
        button.gui.output.append(args[0])

    def close_gui(button: GUI.GUI_Button, *args):
        button.gui.destroy()
        player.guis.remove(button.gui)

    def load_pylon(button: GUI.GUI_Button, *args):
        if button.sub_gui is None:
            button.sub_gui = GUI("weapons", (1, 4), [("sidewinder.png", add_to_output, ["sidewinder"]), ("bomb.png", add_to_output, ["bomb"]), ("pod.png", add_to_output, ["pod"]), ("none.png", add_to_output, [None])], output_len=1, midtop=GUI.Find_GUI(player.guis, "reload").rect.midbottom)
            player.guis.append(button.sub_gui)
        elif button.sub_gui.done:
            button.gui.parent.load_pylon(args[0], button.sub_gui.output[0])
            player.guis.remove(button.sub_gui)
            button.sub_gui.destroy(done=True)
            button.sub_gui = None

    player.guis.append(GUI("reload", (6, 1), [("1.png", load_pylon, [0]), ("2.png", load_pylon, [1]), ("3.png", load_pylon, [2]), ("4.png", load_pylon, [3]), ("5.png", load_pylon, [4]), ("none.png", close_gui, [])], parent=player, callback=stick_to_plane,
                           topleft=player.rect.bottomright))


def main():
    total_timer = 0
    last_time = time.time()
    while True:
        frame_time = time.time() - last_time
        last_time = time.time()
        # Events
        land_group.update()
        runway_group.update()
        blueprint_group.update()
        vehicle_group.update()
        vehicle_projectile_group.update()
        plane_group.update()
        smoke_group.update()
        flare_group.update()
        ordnance_group.update()
        aim_cross_group.update()
        explosion_group.update()
        gui_group.update()
        handle_keys()

        # Timers
        total_timer += 1
        if total_timer % 500 == 0:
            pass
            # F16.spawn_f16()

        # Visual
        screen.fill((1, 201, 250))
        land_group.draw(screen)
        runway_group.draw(screen)
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
        element_group.draw(screen)
        gui_group.draw(screen)

        text2 = score_font.render(f"{round(frame_time * 1000)}ms", True, (255, 255, 255))
        screen.blit(text2, (100, 150))
        text2 = score_font.render(f"{type(player.pylons.cur.data.item)}", True, (255, 255, 255))
        screen.blit(text2, (100, 200))
        text2 = score_font.render(f"{len(gui_group.sprites())}", True, (255, 255, 255))
        screen.blit(text2, (100, 250))

        display.blit(
            pygame.transform.scale(screen, (display.get_width(), display.get_width() * SCREEN_HEIGHT / SCREEN_WIDTH))
            , (0, 0))

        # Refresh
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
