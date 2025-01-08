from math import atan2, sin, cos
import os
import sys
import pygame


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Laser(pygame.sprite.Sprite):
    leftimage = load_image("laser.png")

    def __init__(self, screen, x, y, direction, *group):
        self.x = x
        self.y = y
        self.direction = direction
        super().__init__(*group)
        if self.direction == 'left':
            self.image = Laser.leftimage
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width() / 2, screen.get_height() / 2)


class Cannon(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, *group):
        self.x = x
        self.y = y
        self.direction = direction
        super().__init__(*group)


class LaserCannon(Cannon):
    leftimage = load_image("laser_cannon.png")

    def __init__(self, screen, x, y, direction, *group):
        super().__init__(screen, x, y, direction, *group)
        if self.direction == 'left':
            self.image = LaserCannon.leftimage
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width() / 2, screen.get_height() / 2)

    def shoot(self):
        Laser(self.x, self.y, self.direction, projectiles)



projectiles = pygame.sprite.Group()
