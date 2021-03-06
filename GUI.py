from settings import *
from DataStructs import LinkedCircle


class GUI(pygame.sprite.Sprite):
    @classmethod
    def Find_GUI(cls, guis, gui_id: str):
        for gui in guis:
            if gui.gui_id == gui_id:
                return gui
        return None

    class GUI_Button(pygame.sprite.Sprite):
        def __init__(self, gui, relative_pos, filepath: str, on_click: callable = None, on_click_args: list = None):
            pygame.sprite.Sprite.__init__(self)
            self.gui = gui
            self.relative_pos = relative_pos
            self.callback = on_click
            self.callback_args = on_click_args
            self.sub_gui = None
            self.cache = None
            self.image = pygame.transform.scale(pygame.image.load(f"Assets/buttons/{filepath}").convert_alpha(), self.gui.box_size)
            self.rect = self.image.get_rect(topleft=pygame.math.Vector2(gui.rect.topleft) + relative_pos)

            gui_group.add(self)

        def update(self) -> None:
            if self.sub_gui is not None and self.sub_gui.done:
                self.callback_f()
            self.rect.topleft = pygame.math.Vector2(self.gui.rect.topleft) + self.relative_pos
            if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(relative_mouse()):
                self.callback_f()

        def callback_f(self):
            self.callback(self, *self.callback_args)

        def destroy(self):
            if self.sub_gui is not None:
                self.sub_gui.destroy()
            self.kill()

    class GUI_Selector(pygame.sprite.Sprite):
        def __init__(self, gui):
            super().__init__()
            self.gui = gui
            self.image = pygame.Surface(gui.box_size)
            self.image.fill("Green")
            self.image.set_alpha(160)
            self.rect = self.image.get_rect(topleft=pygame.math.Vector2(gui.rect.topleft))

            gui_group.add(self)

        def update(self) -> None:
            self.rect.topleft = pygame.math.Vector2(self.gui.buttons.cur.data.rect.topleft)

    def __init__(self, gui_id: str, size: tuple[int, int], content: list[tuple[str, callable, list]] = None,
                 box_size: tuple[int, int] = (60, 60), output_len: int = None, parent=None, callback: callable = None, callback_args=None, **pos):
        super().__init__()
        if callback_args is None:
            callback_args = []
        self.output = []
        self.output_len = output_len
        self.done = False
        self.gui_id = gui_id
        self.pos_args = pos
        self.parent = parent
        self.callback = callback
        self.callback_args = callback_args
        self.workspace = {}
        self.box_size = pygame.math.Vector2(box_size)
        self.image = pygame.Surface((self.box_size[0] * size[0], self.box_size[1] * size[1]))
        self.image.fill("green")
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(**self.pos_args)
        if content is None:
            self.content = LinkedCircle(("1.png", "Sidewinder"), ("2.png", "Bomb"), ("3.png", 3), ("4.png", 4))
        else:
            self.content = LinkedCircle(*content)
        self.buttons = LinkedCircle()

        counter = 0
        cur = self.content.head
        while True:
            x = counter % size[0]
            y = counter // size[0]
            button = self.GUI_Button(self, (x * self.box_size.x, y * self.box_size.y), filepath=cur.data[0],
                                     on_click=cur.data[1], on_click_args=cur.data[2])
            self.buttons.add(button)

            cur = cur.next_node
            counter += 1
            if counter >= size[0] * size[1]:
                break

        self.selector = self.GUI_Selector(self)
        gui_group.add(self)

    def destroy(self, done=False):
        cur = self.buttons.head
        while True:
            cur.data.destroy()
            cur = cur.next_node
            if cur == self.buttons.head:
                break
        self.done = done
        self.selector.kill()
        self.kill()

    def set_rect(self, **kwargs):
        self.pos_args = kwargs

    def update(self) -> None:
        if isinstance(self.output_len, int) and len(self.output) >= self.output_len:
            self.done = True
        if self.callback is not None:
            self.callback(self, *self.callback_args)
        self.rect = self.image.get_rect(**self.pos_args)


gui_group = pygame.sprite.Group()
