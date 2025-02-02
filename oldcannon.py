import pygame
import os
import sys
import time
import random
from cannon import Cannon
from projectiles import CannonBall


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class OldCannon(Cannon):
    image = load_image("old_cannon.png")

    def __init__(self, screen, grid, pos, direction, can_rotate, player, *group):
        super().__init__(screen, grid, pos, direction, can_rotate, player, *group)
        self.image = pygame.transform.rotate(OldCannon.image, 90 * self.direction)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.place()
        self.time = time.time()
        self.dir_flag = False
        self.shoot()

    def change_image(self, image, angle):
        x, y = self.rect.centerx, self.rect.centery
        self.image = pygame.transform.rotate(image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self):
        if self.direction == 0:
            self.pos[0] -= 1
        if self.direction == 1:
            self.pos[1] += 1
        if self.direction == 2:
            self.pos[0] += 1
        if self.direction == 3:
            self.pos[1] -= 1

    def update(self, fps):
        self.rect.left, self.rect.top = self.place()
        self.on_screen(self.rect.left + self.image.get_width() / 2, self.rect.top + self.image.get_height() / 2)
        if time.time() - self.time >= 4:
            self.shoot()
            self.time = time.time()
            self.dir_flag = False
        if 2 <= time.time() - self.time and self.can_rotate and not self.dir_flag:
            self.direction = random.choice([0, 1, 2, 3])
            self.change_image(OldCannon.image, self.direction * 90)
            self.dir_flag = True

    def shoot(self):
        self.change_image(OldCannon.image, self.direction * 90)
        CannonBall(self.screen, self.grid, [self.pos[0] + 0.5, self.pos[1] + 0.5], self.direction, self.player,
                *self.groups())