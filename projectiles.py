import os
import sys
import pygame
import time
from math import sqrt


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Laser(pygame.sprite.Sprite):
    image = load_image("laser.png")

    def __init__(self, screen, grid, pos, direction, player, cannon, *group):
        self.cannon = cannon
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

    def update(self, fps):
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
        if not self.cannon.alive():
            self.kill()

    def place(self):
        x = self.grid.center[0] + self.pos[0] * self.grid.cell_size
        y = self.grid.center[1] + self.pos[1] * self.grid.cell_size
        return x, y


class PermaLaser(pygame.sprite.Sprite):
    image = load_image("perma_laser.png")

    def __init__(self, screen, grid, pos, direction, player, cannon, *group):
        self.cannon = cannon
        self.screen = screen
        self.grid = grid
        self.pos = pos
        self.direction = direction
        self.image = pygame.transform.rotate(PermaLaser.image, 90 * self.direction)
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

    def update(self, fps):
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
        if not self.cannon.alive():
            self.kill()

    def place(self):
        x = self.grid.center[0] + self.pos[0] * self.grid.cell_size
        y = self.grid.center[1] + self.pos[1] * self.grid.cell_size
        return x, y


class CannonBall(pygame.sprite.Sprite):
    image = load_image("ball.png")

    def __init__(self, screen, grid, pos, direction, player, *group):
        self.screen = screen
        self.grid = grid
        self.pos = pos
        self.direction = direction
        self.rect = self.image.get_rect()
        self.time = time.time()
        self.player = player
        self.mask = pygame.mask.from_surface(self.image)
        if self.direction == 0:
            self.v = [-4, 0]
        if self.direction == 1:
            self.v = [0, 4]
        if self.direction == 2:
            self.v = [4, 0]
        if self.direction == 3:
            self.v = [0, -4]
        self.rect.center = self.place()
        super().__init__(*group)

    def update(self, fps):
        self.pos[0] += self.v[0] / fps
        self.pos[1] += self.v[1] / fps
        if time.time() - self.time >= 20:
            self.kill()
        self.rect.center = self.place()
        if pygame.sprite.collide_mask(self, self.player):
            self.player.kill()

    def place(self):
        x = self.grid.center[0] + self.pos[0] * self.grid.cell_size
        y = self.grid.center[1] + self.pos[1] * self.grid.cell_size
        return x, y


class MortarShot(pygame.sprite.Sprite):
    image = load_image("ball.png")

    def __init__(self, screen, grid, pos, direction, player, *group):
        self.screen = screen
        self.grid = grid
        self.pos = pos
        self.direction = direction
        self.rect = self.image.get_rect()
        self.time = time.time()
        self.player = player
        self.mask = pygame.mask.from_surface(self.image)
        if self.direction == 0:
            self.v = [-4, 0]
        if self.direction == 1:
            self.v = [0, 4]
        if self.direction == 2:
            self.v = [4, 0]
        if self.direction == 3:
            self.v = [0, -4]
        self.rect.center = self.place()
        super().__init__(*group)

    def update(self, fps):
        self.pos[0] += self.v[0] / fps
        self.pos[1] += self.v[1] / fps
        if time.time() - self.time >= 1:
            Explosion(self.screen, self.grid, self.pos, self.player, self.groups())
            self.kill()
        self.rect.center = self.place()

    def place(self):
        x = self.grid.center[0] + self.pos[0] * self.grid.cell_size
        y = self.grid.center[1] + self.pos[1] * self.grid.cell_size
        return x, y


class Grenade(pygame.sprite.Sprite):
    image = load_image("grenade.png")

    def __init__(self, screen, grid, pos, direction, *group):
        self.screen = screen
        self.grid = grid
        self.pos = pos
        self.direction = direction
        self.rect = self.image.get_rect()
        self.time = time.time()
        self.mask = pygame.mask.from_surface(self.image)
        if self.direction == 0:
            self.v = [-4, 0]
        if self.direction == 0.5:
            self.v = [-2 * sqrt(2), 2 * sqrt(2)]
        if self.direction == 1:
            self.v = [0, 4]
        if self.direction == 1.5:
            self.v = [2 * sqrt(2), 2 * sqrt(2)]
        if self.direction == 2:
            self.v = [4, 0]
        if self.direction == 2.5:
            self.v = [2 * sqrt(2), -2 * sqrt(2)]
        if self.direction == 3:
            self.v = [0, -4]
        if self.direction == 3.5:
            self.v = [-2 * sqrt(2), -2 * sqrt(2)]
        self.rect.center = self.place()
        super().__init__(*group)

    def update(self, fps):
        self.pos[0] += self.v[0] / fps
        self.pos[1] += self.v[1] / fps
        if time.time() - self.time >= 3:
            self.kill()
        self.rect.center = self.place()

    def place(self):
        x = self.grid.center[0] + self.pos[0] * self.grid.cell_size
        y = self.grid.center[1] + self.pos[1] * self.grid.cell_size
        return x, y


class Explosion(pygame.sprite.Sprite):
    image = load_image("explosion.png")

    def __init__(self, screen, grid, pos, player, *group):
        self.screen = screen
        self.grid = grid
        self.pos = pos
        self.player = player
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self.place()
        self.time = time.time()
        super().__init__(*group)

    def update(self, fps):
        if time.time() - self.time >= 2:
            self.kill()
        if pygame.sprite.collide_mask(self, self.player):
            self.player.kill()
        self.rect.centerx, self.rect.centery = self.place()

    def place(self):
        x = self.grid.center[0] + self.pos[0] * self.grid.cell_size
        y = self.grid.center[1] + self.pos[1] * self.grid.cell_size
        return x, y
