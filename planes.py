from settings import *
from effects import Flare, Smoke
from Ordnance import Bomb, Sidewinder, Gun_Pod
from island import runway_group
from DataStructs import LinkedCircle
from GUI import GUI


class ShowElement(pygame.sprite.Sprite):
    def __init__(self, pos, special=False):
        super().__init__()
        self.image = pygame.Surface((20, 5)).convert_alpha()
        if special:
            self.image.fill('red')
        else:
            self.image.fill('green')
        self.rect = self.image.get_rect(center=pos)


class Path:
    __slots__ = ('waypoint_index', 'path')

    class Waypoint:
        def __init__(self, x_pos, y_pos):
            self.pos = x_pos, y_pos

        def x(self) -> int or float:
            return self.pos[0]

        def y(self) -> int or float:
            return self.pos[1]

    def __init__(self, x=0, y=SCREEN_HEIGHT / 2, n_splits=3):
        self.waypoint_index = 0
        self.path = []
        diversion_amount = 1000
        for i in range(int(SCREEN_WIDTH / n_splits)):
            if not self.path:
                self.path.append(self.Waypoint(x_pos=x, y_pos=y))
            else:
                temp_y = self.path[-1].y() + random.randint(-diversion_amount, diversion_amount)
                if temp_y > (screen.get_height() / 10) * 9:
                    temp_y = (screen.get_height() / 10) * 9
                elif temp_y < (screen.get_width() / 10):
                    temp_y = (screen.get_width() / 10)
                self.path.append(self.Waypoint(x_pos=x + (SCREEN_WIDTH / n_splits) * i, y_pos=temp_y))

    def selected_waypoint(self) -> Waypoint:
        return self.path[self.waypoint_index]

    def next_waypoint(self) -> None:
        self.waypoint_index += 1


class AimRetical(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = (-100, 100)
        self.angle = 0
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
            if self.item:
                self.item.deploy()

        def pos_call(self) -> tuple[float, float]:
            v = self.offset.rotate(self.carrier.angle)
            x = self.carrier.rect.centerx + v[0]
            y = self.carrier.rect.centery - v[1]
            return x, y

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
        self.speed = 2
        self.image = pygame.transform.rotozoom(self.stored, 0, self.size)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.flare_timer = 0

    def update_image(self):
        self.image = pygame.transform.rotozoom(self.stored, self.angle, self.size)
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)

    def face_to(self, ang, speed=5.0):
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

    def over_runway(self) -> bool:
        return bool(overlaps_with(self, runway_group))

    def accelerate(self) -> None:
        self.speed = min(self.speed + 0.02, 2)

    def decelerate(self) -> None:
        self.speed = max(self.speed - 0.01, 0)

    def flare(self) -> None:
        Flare.add_flare(self.rect.center, self.threats)


class Player(Plane):
    def __init__(self, pos, angle=0):
        super().__init__(img_path="Assets/Planes/SU25.png")
        self.pos = pygame.math.Vector2(pos)
        self.angle = angle
        self.landed = False
        self.aim_cross = AimRetical()
        self.pylons = LinkedCircle(self.Pylon(self, (0.0, 0.0)),
                                   self.Pylon(self, (-5.0, 10.0)),
                                   self.Pylon(self, (-5.0, -10.0)),
                                   self.Pylon(self, (-5.0, 20.0)),
                                   self.Pylon(self, (-5.0, -20.0)))
        self.default_layout = ("Pod", "sidewinder", "sidewinder", "sidewinder", "sidewinder")
        self.guis = []
        self.reload(*self.default_layout)

    def set_aim_cross(self):
        item = self.pylons.cur.data.item
        if type(item) == Bomb:
            v = pygame.math.Vector2((0.2 - 0.14) / 0.0005 * self.speed * 0.75, 0).rotate(self.angle)
            pos = self.pylons.cur.data.pos_call()
            x = pos[0] + v[0]
            y = pos[1] - v[1]
            self.aim_cross.pos = (x, y)
        elif type(item) == Sidewinder:
            lock = self.pylons.cur.data.item.lock_target()
            if lock is not None:
                self.aim_cross.pos = lock.pos
            else:
                self.aim_cross.pos = (-100, -100)
        elif type(item) == Gun_Pod:
            lock = closest_target(self, plane_group.sprites(), max_range=650, angle_limit=90, exclude=self)
            if lock is not None:
                self.aim_cross.pos = predicted_los(self, lock, 5)
            else:
                self.aim_cross.pos = (-100, -100)
        else:
            self.aim_cross.pos = (-100, -100)

    def destroy_pylons(self):
        cur = self.pylons.head

        while True:
            cur.data.item.kill()
            cur.data.item = None
            cur = cur.next
            if cur == self.pylons.head:
                break

    def reload(self, *weapons):
        self.pylons.cur = self.pylons.head
        for weapon in weapons:
            if self.pylons.cur.data.item is not None:
                self.pylons.cur.data.item.kill()
                self.pylons.cur.data.item = None
            match weapon:
                case "bomb" | "Bomb":
                    self.pylons.cur.data.load(Bomb(self, self.pylons.cur))
                case "sidewinder" | "Sidewinder":
                    self.pylons.cur.data.load(Sidewinder(self, self.pylons.cur, plane_group))
                case "pod" | "Pod":
                    self.pylons.cur.data.load(Gun_Pod(self, self.pylons.cur, plane_group))
                case None:
                    pass
            self.pylons.next()
            if self.pylons.cur == self.pylons.head:
                break

    def load_pylon(self, pylon: int, weapon: str):
        cur = self.pylons.head
        for i in range(pylon):
            cur = cur.next_node
        if cur.data.item is not None:
            cur.data.item.kill()
            cur.data.item = None
        match weapon:
            case "bomb" | "Bomb":
                cur.data.load(Bomb(self, cur))
            case "sidewinder" | "Sidewinder":
                cur.data.load(Sidewinder(self, cur, plane_group))
            case "pod" | "Pod":
                cur.data.load(Gun_Pod(self, cur, plane_group))
            case None:
                pass

    def update(self):
        if self.over_runway():
            keyboard = pygame.key.get_pressed()
            if keyboard[pygame.K_s]:
                self.decelerate()
            elif keyboard[pygame.K_w]:
                self.accelerate()

            if self.speed == 0 and not self.landed:
                self.landed = True
            elif self.speed != 0:
                self.landed = False
        else:
            if self.speed < 2:
                self.accelerate()
        self.face_to(relative_mouse(), speed=self.speed * 2.5)
        self.move(self.speed)
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
        self.path = Path(y=self.pos[1], n_splits=3)
        # self.draw_path()

    def draw_path(self):
        for point in self.path.path:
            element_group.add(ShowElement(point.pos))

    def update(self):
        if self.rect.centerx > self.path.selected_waypoint().x():
            self.path.next_waypoint()
        self.face_to(self.path.selected_waypoint().pos, speed=1)
        self.flare_timer += 1
        if self.threats and self.flare_timer % 30 == 0:
            self.flare()

        self.move(2)
        self.check_out_of_bounds()
        self.update_image()
        self.check_health()


aim_cross_group = pygame.sprite.Group()
plane_group = pygame.sprite.Group()
element_group = pygame.sprite.Group()
player = Player(pos=(screen.get_width(), SCREEN_HEIGHT / 2), angle=180)
plane_group.add(player)
