import os
import sys
import pygame
import time
import random


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Laser(pygame.sprite.Sprite):
    image = load_image("laser.png")

    def __init__(self, screen, grid, pos, direction, player, *group):
        self.screen = screen
        self.grid = grid
        self.pos = pos
        self.direction = direction
        self.image = pygame.transform.rotate(Laser.image, 90 * self.direction)
        self.rect = self.image.get_rect()
        self.time = time.time()
        self.player = player
        self.mask = pygame.mask.from_surface(self.image)
        if self.direction == 0:
            self.rect.midright = self.place()
        if self.direction == 1:
            self.rect.midtop = self.place()
        if self.direction == 2:
            self.rect.midleft = self.place()
        if self.direction == 3:
            self.rect.midbottom = self.place()
        super().__init__(*group)

    def update(self):
        if time.time() - self.time >= 2:
            self.kill()
        if self.direction == 0:
            self.rect.midright = self.place()
        if self.direction == 1:
            self.rect.midtop = self.place()
        if self.direction == 2:
            self.rect.midleft = self.place()
        if self.direction == 3:
            self.rect.midbottom = self.place()
        if pygame.sprite.collide_mask(self, self.player):
            self.player.kill()

    def place(self):
        x = self.grid.center[0] + self.pos[0] * self.grid.cell_size
        y = self.grid.center[1] + self.pos[1] * self.grid.cell_size
        return x, y


class Cannon(pygame.sprite.Sprite):
    def __init__(self, screen, grid, pos, direction, player, *group):
        self.screen = screen
        self.grid = grid
        self.pos = pos
        self.direction = direction
        self.player = player
        super().__init__(*group)

    def change_image(self, image, angle):
        x, y = self.rect.centerx, self.rect.centery
        self.image = pygame.transform.rotate(image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def place(self):
        x = self.grid.center[0] + self.pos[0] * self.grid.cell_size
        y = self.grid.center[1] + self.pos[1] * self.grid.cell_size
        return x, y

    def on_screen(self, x, y):
        xp, yp = 0, 0
        if x < 0 or x > self.screen.get_width() or y < 0 or y > self.screen.get_height():
            if x < 0:
                xp = 10
            elif x > self.screen.get_width():
                xp = self.screen.get_width() - 10
            else:
                xp = x
            if y < 0:
                yp = 10
            elif y > self.screen.get_height():
                yp = self.screen.get_height() - 10
            else:
                yp = y
            pygame.draw.circle(self.screen, (220, 0, 0), (xp, yp), 8)


class LaserCannon(Cannon):
    image_off = load_image("laser_cannon_off.png")
    image_on = load_image("laser_cannon_on.png")

    def __init__(self, screen, grid, pos, direction, player, *group):
        super().__init__(screen, grid, pos, direction, player, *group)
        self.image = pygame.transform.rotate(LaserCannon.image_off, 90 * self.direction)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = self.place()
        self.time = time.time()
        self.dir_flag = False

    def update(self):
        self.rect.left, self.rect.top = self.place()
        self.on_screen(self.rect.left + self.image.get_width() / 2, self.rect.top + self.image.get_height() / 2)
        if time.time() - self.time >= 4:
            self.shoot()
            self.time = time.time()
            self.dir_flag = False
        if 2 <= time.time() - self.time and not self.dir_flag:
            self.direction = random.choice([0, 1, 2, 3])
            self.change_image(LaserCannon.image_off, self.direction * 90)
            self.dir_flag = True

    def shoot(self):
        self.change_image(LaserCannon.image_on, self.direction * 90)
        Laser(self.screen, self.grid, (self.pos[0] + 0.5, self.pos[1] + 0.5), self.direction, self.player, *self.groups())



projectiles = pygame.sprite.Group()
