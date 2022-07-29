from settings import *
from planes import plane_group
from effects import Smoke, explosion_group
from island import island
from GUI import GUI


class Blueprint(pygame.sprite.Sprite):
    @classmethod
    def fill(cls, surface, color):
        w, h = surface.get_size()
        r, g, b, _ = color
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pygame.Color(r, g, b, a))

    def __init__(self, obj):
        super().__init__()
        self.obj = obj
        self.image = pygame.Surface.copy(obj.idle)
        self.image.set_alpha(75)
        self.fill(self.image, pygame.Color(10, 40, 250))
        self.rect = self.image.get_rect(center=pygame.mouse.get_pos())
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.center = relative_mouse()

    def place(self):
        global in_hand
        if self.mask.overlap(island.mask, (island.rect.x - self.rect.x, island.rect.y - self.rect.y)):
            vehicle_group.add(self.obj(self.rect.center))
            in_hand = False
            self.kill()


blueprint_group = pygame.sprite.GroupSingle()
in_hand = False


class Vehicle(pygame.sprite.Sprite):
    preview = pygame.image.load('Assets/Vehicles/Grad/preview.png').convert_alpha()
    idle = pygame.transform.rotozoom(pygame.image.load('Assets/Vehicles/Grad/idle.png').convert_alpha(), 0, 0.1)

    def __init__(self):
        super().__init__()
        self.life_span = 0
        self.gui = None

    def take_damage(self, dmg_range=30):
        for explosion in explosion_group.sprites():
            if dis_to(self.rect.center, explosion.rect.center) < dmg_range:
                self.kill()

    def kill(self) -> None:
        super().kill()
        if self.gui is not None:
            self.gui.destroy()

    def spawn_gui_on_click(self):
        def gui_callable(button, *args):
            if args[0] is None:
                button.gui.destroy(done=True)
                button.gui.parent.gui = None
            elif args[0] == 'kill':
                button.gui.destroy(done=True)
                self.kill()
            elif args[0] == 'move':
                button.gui.destroy(done=True)
                self.kill()
                global in_hand
                in_hand = True
                blueprint_group.add(Blueprint(type(self)))

        self.life_span += 1
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(relative_mouse()) and self.gui is None and self.life_span > 30:
            self.gui = GUI("vehicle_menu", (1, 3),
                           content=[("none.png", gui_callable, [None]), ("bin.png", gui_callable, ["kill"]), ("move.png", gui_callable, ["move"])], parent=self,
                           topleft=self.rect.bottomright)


class Grad(Vehicle):
    __slots__ = ('image', 'rect')

    class Missile(pygame.sprite.Sprite):
        def __init__(self, pos):
            super().__init__()
            self.image = pygame.image.load('Assets/bullet.png').convert_alpha()
            self.rect = self.image.get_rect(center=pos)

        def update(self):
            self.rect.x += 1

    preview = pygame.image.load('Assets/Vehicles/Grad/preview.png').convert_alpha()
    idle = pygame.transform.rotozoom(pygame.image.load('Assets/Vehicles/Grad/idle.png').convert_alpha(), 0, 0.1)

    def __init__(self, pos):
        super().__init__()
        self.image = Grad.idle
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.a = Grad.Missile(self.rect.center)
        vehicle_projectile_group.add(self.a)

    def update(self):
        self.spawn_gui_on_click()
        self.take_damage(35)


class Vads(Vehicle):
    __slots__ = ('image', 'rect', 'mask', 'target')

    class VadsBullet(pygame.sprite.Sprite):
        __slots__ = ('stored', 'position', 'image', 'rect', 'mask', 'v')

        def __init__(self, pos, angle):
            super().__init__()
            angle += random.uniform(-5, 5)
            self.stored = pygame.image.load('Assets/bullet.png').convert_alpha()
            self.position = pygame.math.Vector2(pos)
            self.image = pygame.transform.rotozoom(self.stored, angle, 0.1)
            self.rect = self.image.get_rect(center=self.position)
            self.mask = pygame.mask.from_surface(self.image)
            self.v = pygame.math.Vector2((5, 0)).rotate(angle)

        def update(self):
            self.position[0] += self.v[0]
            self.position[1] -= self.v[1]
            self.rect.center = self.position

            for overlap in overlaps_with(self, plane_group.sprites()):
                overlap.health -= 1
                self.kill()

            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH \
                    or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
                self.kill()

    preview = pygame.image.load('Assets/Vehicles/Vads/preview.png').convert_alpha()
    idle = pygame.transform.rotozoom(pygame.image.load('Assets/Vehicles/Vads/idle.png').convert_alpha(), 0, 0.1)

    def __init__(self, pos):
        super().__init__()
        self.image = Vads.idle
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.target = None
        self.gui = None

    def predicted_los(self, target, r=0):
        if target:
            t = dis_to(self.rect.center, self.predicted_los(target, r=r + 1) if r <= 2 else target.rect.center) / 5
            return target.rect.centerx + (target.v[0] * int(t)), target.rect.centery + (
                    -target.v[1] * int(t))
        else:
            return 0

    def shoot(self):
        if self.target:
            vehicle_projectile_group.add(
                self.VadsBullet(self.rect.center, dir_to(self.rect.center, self.predicted_los(self.target))))

    def update(self):
        self.spawn_gui_on_click()
        self.target = closest_target(self, plane_group.sprites(), max_range=250)
        self.shoot()
        self.take_damage(30)


class ManAA(Vehicle):
    class ManAAMissile(pygame.sprite.Sprite):
        def __init__(self, pos, target):
            super().__init__()
            self.pos = pygame.math.Vector2(pos)
            self.stored = pygame.transform.rotozoom(
                pygame.image.load('Assets/Vehicles/ManAA/missile.png').convert_alpha(),
                0, 0.1)
            self.image = pygame.transform.rotate(self.stored, 0)
            self.rect = self.image.get_rect(center=self.pos)
            self.mask = pygame.mask.from_surface(self.image)

            self.target = target
            self.angle = dir_to(self.rect.center, self.target.rect.center)

            self.target.threats.append(self)

            self.speed = 3

            self.burner = 90  # Amount of ticks before the missile slows down.

            self.trash_chance = 0.4

        def predicted_los(self, target, r=0):
            if target:
                t = dis_to(self.rect.center,
                           self.predicted_los(target, r=r + 1) if r <= 2 else target.rect.center) / self.speed
                return target.rect.centerx + (target.v[0] * int(t)), target.rect.centery + (
                        -target.v[1] * int(t))
            else:
                return 0

        def check_for_hit(self):
            for overlap in overlaps_with(self, plane_group.sprites()):
                self.remove_threat()
                overlap.health = 0
                self.kill()

        def remove_threat(self):
            try:
                self.target.threats.remove(self)
            except ValueError:
                pass
            except AttributeError:
                pass

        def check_out_of_bounds(self):
            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
                self.remove_threat()
                self.kill()

        def reduce_speed(self, turn):
            if self.burner <= 0:
                self.speed -= abs(turn) / 50

        def update(self) -> None:
            self.check_for_hit()
            self.check_out_of_bounds()
            if self.target:
                face_to(self, self.predicted_los(self.target), self.speed, f=self.reduce_speed)
                if gimbal_limit(self, dir_to(self.rect.center, self.target.rect.center), 70):
                    self.target = None

            # Slow down the missile
            self.burner -= 1
            if self.burner <= 0:
                self.speed *= 0.999
                if self.speed <= 0.5:
                    self.remove_threat()
                    self.kill()
            else:
                v = pygame.math.Vector2(-10, 0).rotate(self.angle)
                p = self.rect.center
                smoke_vent = (p[0] + v[0], p[1] - v[1])
                Smoke.add_smoke(smoke_vent, spreadx=(-0.2, 0.2), spready=(-0.2, 0.2), size=0.1, opacity=122)

            # Move the missile
            v = pygame.math.Vector2((self.speed, 0)).rotate(self.angle)
            self.pos[0] += v[0]
            self.pos[1] -= v[1]

            # Update
            self.image = pygame.transform.rotate(self.stored, self.angle)
            self.rect = self.image.get_rect(center=self.pos)
            self.mask = pygame.mask.from_surface(self.image)

    preview = pygame.image.load('Assets/Vehicles/ManAA/preview.png').convert_alpha()
    idle = pygame.transform.rotozoom(pygame.image.load('Assets/Vehicles/ManAA/idle.png').convert_alpha(), 0, 0.1)

    def __init__(self, pos):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.stored = ManAA.idle
        self.image = pygame.transform.rotate(self.stored, 0)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.target = None

        self.fire_timer = 0

    def shoot(self):
        if self.target:
            vehicle_projectile_group.add(
                self.ManAAMissile(self.pos, self.target)
            )

    def update(self):
        self.spawn_gui_on_click()
        self.target = closest_target(self, plane_group.sprites(), max_range=350)
        self.fire_timer += 1
        if self.target and self.fire_timer % 300 == 0:
            self.shoot()
        self.take_damage(40)


vehicle_group = pygame.sprite.Group()
vehicle_projectile_group = pygame.sprite.Group()
