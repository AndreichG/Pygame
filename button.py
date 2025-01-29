import pygame


class Button:
    def __init__(self, screen, color, func, x, y, w, h, text='', font=None, id=None):
        self.screen = screen
        self.screen_size = (screen.get_width(), screen.get_height())
        self.color = color
        self.center = [x * self.screen_size[0], y * self.screen_size[1]]
        self.dimensions = [w * self.screen_size[0], h * self.screen_size[1]]
        self.id = id
        self.func = func
        self.text = text
        self.font = pygame.font.Font(font, 50)

    def render(self):
        pygame.draw.rect(self.screen, self.color, (self.center[0] - self.dimensions[0] / 2,
                                                   self.center[1] - self.dimensions[1] / 2,
                                                   self.dimensions[0],
                                                   self.dimensions[1]))
        pygame.draw.rect(self.screen, (0, 0, 0), (self.center[0] - self.dimensions[0] / 2,
                                                   self.center[1] - self.dimensions[1] / 2,
                                                   self.dimensions[0],
                                                   self.dimensions[1]), width=3)
        text = self.font.render(self.text, True, (0, 0, 0))
        text_x = self.center[0] - text.get_width() // 2
        text_y = self.center[1] - text.get_height() // 2
        self.screen.blit(text, (text_x, text_y))

    def check(self, pos, key):
        print(pos, key)
        if (key == 1 and
                self.center[0] - self.dimensions[0] / 2 < pos[0] < self.center[0] + self.dimensions[0] / 2 and
                self.center[1] - self.dimensions[1] / 2 < pos[1] < self.center[1] + self.dimensions[1] / 2):
            if self.id is None:
                self.func()
            else:
                self.func(self.id)

    def sc_resize(self):
        x = self.center[0] / self.screen_size[0]
        y = self.center[1] / self.screen_size[1]
        w = self.dimensions[0] / self.screen_size[0]
        h = self.dimensions[1] / self.screen_size[1]
        print(x, y, w, h)
        self.center[0] = self.screen.get_width() * x
        self.center[1] = self.screen.get_height() * y
        self.dimensions[0] = self.screen.get_width() * w
        self.dimensions[1] = self.screen.get_height() * h
        self.screen_size = (self.screen.get_width(), self.screen.get_height())
        self.dimensions = [w * self.screen_size[0], h * self.screen_size[1]]
