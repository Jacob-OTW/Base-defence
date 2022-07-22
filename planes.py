from settings import *
from effects import Flare, Smoke
from Ordnance import Bomb, Sidewinder


class ShowElement(pygame.sprite.Sprite):
    def __init__(self, pos, special=False):
        super().__init__()
        self.image = pygame.image.load('Assets/bullet.png').convert_alpha()
        if special:
            self.image.fill('red')
        self.rect = self.image.get_rect(center=pos)


class Path:
    __slots__ = ('waypoint_index', 'path')

    class Waypoint:
        def __init__(self, x_pos, y_pos):
            self.pos = x_pos, y_pos

        def x(self):
            return self.pos[0]

        def y(self):
            return self.pos[1]

    def __init__(self, x=0, y=SCREEN_HEIGHT / 2, n_splits=3):
        self.waypoint_index = 0
        self.path = []
        diversion_amount = 1000
        for i in range(int(round(SCREEN_WIDTH / n_splits))):
            if not self.path:
                self.path.append(self.Waypoint(x_pos=x, y_pos=y))
            else:
                temp_y = self.path[-1].y() + random.randint(-diversion_amount, diversion_amount)
                while temp_y < 0 or temp_y > SCREEN_HEIGHT:
                    temp_y = self.path[-1].y() + random.randint(-diversion_amount, diversion_amount)
                self.path.append(self.Waypoint(x_pos=x + (SCREEN_WIDTH / n_splits) * i, y_pos=temp_y))

    def selected_waypoint(self):
        return self.path[self.waypoint_index]

    def next_waypoint(self):
        self.waypoint_index += 1


class AimRetical(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = (-100, 100)
        self.image = pygame.transform.rotozoom(pygame.image.load('Assets/AimCross.png'), 0, 0.4).convert_alpha()
        self.image.set_alpha(255 / 2)
        self.rect = self.image.get_rect(center=self.pos)

        aim_cross_group.add(self)

    def update(self):
        self.rect.center = self.pos


class Plane(pygame.sprite.Sprite):
    class Pylon:
        def __init__(self, carrier, offset):
            self.offset = pygame.math.Vector2(offset)
            self.carrier = carrier
            self.item = None
            self.pos = (0, 0)

        def load(self, obj):
            self.item = obj

        def fire(self):
            self.item.deploy()
            self.item = None

        def pos_call(self):
            v = self.offset.rotate(self.carrier.angle)
            x = self.carrier.rect.centerx + v[0]
            y = self.carrier.rect.centery - v[1]
            return x, y

    element_group = pygame.sprite.Group()
    __slots__ = ('position', 'angle', 'v', 'health', 'stored', 'size', 'image', 'rect', 'mask', 'flare_timer', 'pylons')

    def __init__(self, pos=(0, 0), angle=0, img_path='Assets/Planes/F16.png'):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.angle = angle
        self.v = pygame.math.Vector2((0, 0))
        self.health = 100
        self.threats = []
        self.stored = pygame.image.load(img_path).convert_alpha()
        self.size = 0.3
        self.image = pygame.transform.rotozoom(self.stored, 0, self.size)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.flare_timer = 0

    def update_image(self):
        self.image = pygame.transform.rotozoom(self.stored, self.angle, self.size)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def face_to(self, ang, speed=5):
        angle = dir_to(self.rect.center, ang)
        self.angle += math.sin(math.radians(angle - self.angle)) * speed

    def destroy(self):
        self.kill()

    def move(self, amount):
        self.v = pygame.math.Vector2((amount, 0)).rotate(self.angle)
        self.pos.x += self.v[0]
        self.pos.y -= self.v[1]

    def check_out_of_bounds(self):
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.destroy()

    def check_health(self):
        if self.health <= 0:
            self.destroy()

    def flare(self):
        Flare.add_flare(self.rect.center, self.threats)


class Player(Plane):
    def __init__(self, pos, angle=0):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.angle = angle
        self.aim_cross = AimRetical()
        self.pylons = [self.Pylon(self, (-10.0, -10.0)), self.Pylon(self, (-10.0, 10.0))]
        for i, pylon in enumerate(self.pylons):
            pylon.load(Bomb(self, i))

    def set_aim_cross(self):
        selected_pylon = None
        for pylon in self.pylons:
            if type(pylon.item) is Bomb:
                selected_pylon = pylon
                break
        if selected_pylon:
            v = pygame.math.Vector2((0.2 - 0.14) / 0.0005 * 1.5, 0).rotate(self.angle)
            pos = selected_pylon.pos_call()
            x = pos[0] + v[0]
            y = pos[1] - v[1]
            self.aim_cross.pos = (x, y)
        else:
            aim_cross_group.sprites()[0].pos = (-100, -100)

    def destroy_pylons(self):
        for pylon in self.pylons:
            if pylon.item:
                pylon.item.kill()

    def update(self):
        self.face_to(relative_mouse())
        self.move(2)
        self.check_out_of_bounds()
        self.set_aim_cross()
        self.update_image()


class F16(Plane):
    @classmethod
    def spawn_f16(cls):
        plane_group.add(F16(pos=(0, random.randint(50, SCREEN_HEIGHT - 50)), angle=0))

    def __init__(self, pos, angle):
        super(F16, self).__init__()
        self.pos = pygame.math.Vector2(pos)
        self.angle = angle
        self.path = Path(y=self.pos[1])
        for point in self.path.path:
            Plane.element_group.add(ShowElement(point.pos))

    def update(self):
        if self.rect.centerx > self.path.selected_waypoint().x():
            self.path.next_waypoint()
        self.flare_timer += 1
        if self.threats and self.flare_timer % 30 == 0:
            self.flare()
        self.face_to(self.path.selected_waypoint().pos, speed=1)
        self.move(2)
        self.check_out_of_bounds()
        self.update_image()
        self.check_health()


aim_cross_group = pygame.sprite.Group()
plane_group = pygame.sprite.Group()
plane_group.add(Player(pos=(0, SCREEN_HEIGHT / 2)))
