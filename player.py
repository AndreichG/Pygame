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

    def __init__(self, screen, grid, fps, *group):
        super().__init__(*group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.p0 = self.rect.center
        self.v = 256 / fps

        self.screen = screen
        self.grid = grid
        self.screen_size = (screen.get_width(), screen.get_height())
        self.pos = (0, 0)
        self.rect.topleft = self.place()

    def update(self):
        self.move()
        self.check()

    def place(self):
        x = self.grid.center[0] + self.pos[0] * self.grid.cell_size
        y = self.grid.center[1] + self.pos[1] * self.grid.cell_size
        return x, y

    def change_image(self, image, angle):
        x, y = self.rect.centerx, self.rect.centery
        self.image = pygame.transform.rotate(image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if keys[pygame.K_a]:
                self.change_image(Player.image, 45)
                self.rect.x += -self.v * cos(pi / 4)
                self.rect.y += -self.v * sin(pi / 4)
                print(1)
            elif keys[pygame.K_d]:
                self.change_image(Player.image, -45)
                self.rect.x += self.v * cos(pi / 4)
                self.rect.y += -self.v * sin(pi / 4)
                print(2)
            else:
                self.change_image(Player.image, 0)
                self.rect.y += -self.v
                print(3)

        elif keys[pygame.K_s]:
            if keys[pygame.K_a]:
                self.change_image(Player.image, 135)
                self.rect.x += -self.v * cos(pi / 4)
                self.rect.y += self.v * sin(pi / 4)
                print(4)
            elif keys[pygame.K_d]:
                self.change_image(Player.image, -135)
                self.rect.x += self.v * cos(pi / 4)
                self.rect.y += self.v * sin(pi / 4)
                print(5)
            else:
                self.change_image(Player.image, 180)
                self.rect.y += self.v
                print(6)

        elif keys[pygame.K_a] and not (keys[pygame.K_w] and keys[pygame.K_s]):
            self.change_image(Player.image, 90)
            self.rect.x += -self.v
            print(7)

        elif keys[pygame.K_d] and not (keys[pygame.K_w] and keys[pygame.K_s]):
            self.change_image(Player.image, -90)
            self.rect.x += self.v
            print(7)


        self.pos = (self.rect.centerx - self.grid.center[0], self.rect.centery - self.grid.center[1])

    def check(self):
        dx, dy = 0, 0
        if self.rect.centerx < int(self.screen.get_width() / 4):
            dx = self.rect.centerx - int(self.screen.get_width() / 4)
            self.rect.centerx = int(self.screen.get_width() / 4)
        if self.rect.centerx > int(self.screen.get_width() / 4 * 3):
            dx = self.rect.centerx - int(self.screen.get_width() / 4 * 3)
            self.rect.centerx = int(self.screen.get_width() / 4 * 3)
        if self.rect.centery < int(self.screen.get_height() / 4):
            dy = self.rect.centery - int(self.screen.get_height() / 4)
            self.rect.centery = int(self.screen.get_height() / 4)
        if self.rect.centery > int(self.screen.get_height() / 4 * 3):
            dy = self.rect.centery - int(self.screen.get_height() / 4 * 3)
            self.rect.centery = int(self.screen.get_height() / 4 * 3)
        self.grid.move((dx, dy))

    def sc_resize(self):
        x = self.rect.centerx / self.screen_size[0]
        y = self.rect.centery / self.screen_size[1]
        self.rect.centerx = self.screen.get_width() * x
        self.rect.centery = self.screen.get_height() * y
        self.screen_size = (self.screen.get_width(), self.screen.get_height())
        self.grid.center[0] = self.rect.centerx - self.pos[0]
        self.grid.center[1] = self.rect.centery - self.pos[1]
