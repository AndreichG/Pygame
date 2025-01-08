import os
import sys
from math import sin,cos, pi
import pygame


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Player(pygame.sprite.Sprite):
    image = load_image("player1.png")

    def __init__(self, screen, grid, *group):
        super().__init__(*group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.mask = self.image.get_masks()
        self.p0 = self.rect.center
        self.v = 5

        self.screen = screen
        self.screen_size = (screen.get_width(), screen.get_height())
        self.rect.center = (screen.get_width() / 2, screen.get_height() / 2)
        self.grid = grid
        self.g = (0, 0)

    def rotate(self, angle):
        x, y = self.rect.centerx, self.rect.centery
        self.image = pygame.transform.rotate(Player.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if keys[pygame.K_a]:
                self.rotate(45)
                self.rect.x += -self.v * cos(pi / 4)
                self.rect.y += -self.v * sin(pi / 4)
            elif keys[pygame.K_d]:
                self.rotate(-45)
                self.rect.x += self.v * cos(pi / 4)
                self.rect.y += -self.v * sin(pi / 4)
            else:
                self.rotate(0)
                self.rect.y += -self.v

        elif keys[pygame.K_s]:
            if keys[pygame.K_a]:
                self.rotate(135)
                self.rect.x += -self.v * cos(pi / 4)
                self.rect.y += self.v * sin(pi / 4)
            elif keys[pygame.K_d]:
                self.rotate(-135)
                self.rect.x += self.v * cos(pi / 4)
                self.rect.y += self.v * sin(pi / 4)
            else:
                self.rotate(180)
                self.rect.y += self.v

        elif keys[pygame.K_a] and not (keys[pygame.K_w] and keys[pygame.K_s]):
            self.rotate(90)
            self.rect.x += -self.v

        elif keys[pygame.K_d] and not (keys[pygame.K_w] and keys[pygame.K_s]):
            self.rotate(-90)
            self.rect.x += self.v


        self.g = (self.rect.centerx - self.grid.center[0], self.rect.centery - self.grid.center[1])

    def check(self):
        dx, dy = 0, 0
        if self.rect.centerx < int(self.screen.get_width() / 5):
            dx = self.rect.centerx - int(self.screen.get_width() / 5)
            self.rect.centerx = int(self.screen.get_width() / 5)
        if self.rect.centerx > int(self.screen.get_width() / 5 * 4):
            dx = self.rect.centerx - int(self.screen.get_width() / 5 * 4)
            self.rect.centerx = int(self.screen.get_width() / 5 * 4)
        if self.rect.centery < int(self.screen.get_height() / 5):
            dy = self.rect.centery - int(self.screen.get_height() / 5)
            self.rect.centery = int(self.screen.get_height() / 5)
        if self.rect.centery > int(self.screen.get_height() / 5 * 4):
            dy = self.rect.centery - int(self.screen.get_height() / 5 * 4)
            self.rect.centery = int(self.screen.get_height() / 5 * 4)
        print(self.rect.centery, int(self.screen.get_height() / 5 * 4))
        self.grid.move((dx, dy))

    def sc_resize(self):
        x = self.rect.centerx / self.screen_size[0]
        y = self.rect.centery / self.screen_size[1]
        self.rect.centerx = self.screen.get_width() * x
        self.rect.centery = self.screen.get_height() * y
        self.screen_size = (self.screen.get_width(), self.screen.get_height())
        self.grid.center[0] = self.rect.centerx - self.g[0]
        self.grid.center[1] = self.rect.centery - self.g[1]
