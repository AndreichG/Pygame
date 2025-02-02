import pygame
import os
import sys
import time
import random
from cannon import Cannon


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Mortar(Cannon):
    image = load_image("mortar.png")

    def __init__(self, screen, grid, pos, direction, can_rotate, *group):
        super().__init__(screen, grid, pos, direction, can_rotate, *group)
        self.image = pygame.transform.rotate(Mortar.image, 90 * self.direction)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.place()
        self.time = time.time()
        self.dir_flag = False

    def change_image(self, image, angle):
        x, y = self.rect.centerx, self.rect.centery
        self.image = pygame.transform.rotate(image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, fps):
        self.rect.left, self.rect.top = self.place()
        self.on_screen(self.rect.left + self.image.get_width() / 2, self.rect.top + self.image.get_height() / 2)
        if time.time() - self.time >= 4:
            self.time = time.time()
            self.dir_flag = False
        if 2 <= time.time() - self.time and not self.dir_flag:
            if self.can_rotate:
                self.direction = random.choice([0, 1, 2, 3])
            self.change_image(Mortar.image, self.direction * 90)
            self.dir_flag = True
