import pygame
import os
import sys


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Button:
    def __init__(self, screen, func, x, y, w, h, color=(255, 255, 255), text='', font=None, arg=None):
        self.screen = screen
        self.screen_size = (screen.get_width(), screen.get_height())
        self.color = color
        self.center = [x * self.screen_size[0], y * self.screen_size[1]]
        self.dimensions = [w * self.screen_size[0], h * self.screen_size[1]]
        self.arg = arg
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
        if (key == 1 and
                self.center[0] - self.dimensions[0] / 2 < pos[0] < self.center[0] + self.dimensions[0] / 2 and
                self.center[1] - self.dimensions[1] / 2 < pos[1] < self.center[1] + self.dimensions[1] / 2):
            if self.arg is None:
                self.func()
            else:
                self.func(self.arg)

    def sc_resize(self):
        x = self.center[0] / self.screen_size[0]
        y = self.center[1] / self.screen_size[1]
        w = self.dimensions[0] / self.screen_size[0]
        h = self.dimensions[1] / self.screen_size[1]
        self.center[0] = self.screen.get_width() * x
        self.center[1] = self.screen.get_height() * y
        self.dimensions[0] = self.screen.get_width() * w
        self.dimensions[1] = self.screen.get_height() * h
        self.screen_size = (self.screen.get_width(), self.screen.get_height())
        self.dimensions = [w * self.screen_size[0], h * self.screen_size[1]]


class ImageButton(Button):
    def __init__(self, screen, func, x, y, image, arg=None):
        self.image0 = load_image(image)
        self.image = self.image0
        self.rect = self.image.get_rect()
        self.screen = screen
        self.rect.center = x * self.screen.get_width(), y * self.screen.get_height()
        w, h = self.rect.width / self.screen.get_width(), self.rect.height / self.screen.get_height()
        super().__init__(screen, func, x, y, w, h, arg=arg)

    def render(self):
        self.screen.blit(self.image, self.rect.topleft)

    def check(self, pos, key):
        print(pos, key, self.center, self.dimensions)
        super().check(pos, key)


    def scale_image(self, scale0 = None):
        x, y = self.rect.centerx, self.rect.centery
        if scale0 is not None:
            self.image = pygame.transform.scale(self.image0, (self.dimensions[0] / scale0[0] * self.screen.get_width(), self.dimensions[1] / scale0[1] * self.screen.get_height()))
        else:
            self.image = pygame.transform.scale(self.image0, self.dimensions)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def sc_resize(self):
        x = self.center[0] / self.screen_size[0]
        y = self.center[1] / self.screen_size[1]
        w = self.dimensions[0] / self.screen_size[0]
        h = self.dimensions[1] / self.screen_size[1]
        self.center[0] = self.screen.get_width() * x
        self.center[1] = self.screen.get_height() * y
        self.dimensions[0] = self.screen.get_width() * w
        self.dimensions[1] = self.screen.get_height() * h
        self.rect.center = x * self.screen.get_width(), y * self.screen.get_height()
        self.scale_image()
        self.screen_size = (self.screen.get_width(), self.screen.get_height())