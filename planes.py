from settings import *
from effects import Flare


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


class Plane(pygame.sprite.Sprite):
    element_group = pygame.sprite.Group()
    __slots__ = ('position', 'angle', 'v', 'health', 'stored', 'size', 'image', 'rect', 'mask', 'flare_timer')

    def __init__(self, pos=(0, 0), angle=0, img_path='Assets/Planes/F16.png', is_bot=False):
        super().__init__()
        self.position = pygame.math.Vector2(pos)
        self.angle = angle
        self.v = pygame.math.Vector2((0, 0))
        self.health = 100
        self.threats = []
        self.stored = pygame.image.load(img_path).convert_alpha()
        self.size = 0.3
        self.image = pygame.transform.rotozoom(self.stored, 0, self.size)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)
        self.flare_timer = 0

        # Path
        if is_bot:
            self.path = Path(y=self.position[1])
            for point in self.path.path:
                Plane.element_group.add(ShowElement(point.pos))

    def rotate_img(self):
        self.image = pygame.transform.rotozoom(self.stored, self.angle, self.size)
        self.rect = self.image.get_rect(center=self.position)
        self.mask = pygame.mask.from_surface(self.image)

    def face_to(self, ang, speed=5):
        angle = dir_to(self.rect.center, ang)
        self.angle += math.sin(math.radians(angle - self.angle)) * speed

    def move(self, amount):
        self.v = pygame.math.Vector2((amount, 0)).rotate(self.angle)
        self.position[0] += self.v[0]
        self.position[1] -= self.v[1]
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def check_health(self):
        if self.health <= 0:
            self.kill()

    def flare(self):
            Flare.add_flare(self.rect.center, self.threats)

    def update(self):
        self.face_to(pygame.mouse.get_pos())
        self.move(2)
        self.rotate_img()


class F16(Plane):
    @classmethod
    def spawn_f16(cls):
        plane_group.add(F16(pos=(0, random.randint(50, SCREEN_HEIGHT - 50)), angle=0, is_bot=True))

    def update(self):
        if self.rect.centerx > self.path.selected_waypoint().x():
            self.path.next_waypoint()
        self.flare_timer += 1
        if self.threats and self.flare_timer % 30 == 0:
            self.flare()
        self.face_to(self.path.selected_waypoint().pos, speed=1)
        self.move(2)
        self.rotate_img()
        self.check_health()


plane_group = pygame.sprite.Group(Plane(pos=(0, SCREEN_HEIGHT / 2)))
