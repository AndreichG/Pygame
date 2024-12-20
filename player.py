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

    def __init__(self, screen, *group):
        super().__init__(*group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width() / 2, screen.get_height() / 2)
        self.v = 5

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if keys[pygame.K_a]:
                self.image = pygame.transform.rotate(Player.image, 45)
                self.rect.x += -self.v * cos(pi / 4)
                self.rect.y += -self.v * sin(pi / 4)
            elif keys[pygame.K_d]:
                self.image = pygame.transform.rotate(Player.image, -45)
                self.rect.x += self.v * cos(pi / 4)
                self.rect.y += -self.v * sin(pi / 4)
            else:
                self.image = pygame.transform.rotate(Player.image, 0)
                self.rect.y += -self.v

        elif keys[pygame.K_s]:
            if keys[pygame.K_a]:
                self.image = pygame.transform.rotate(Player.image, 135)
                self.rect.x += -self.v * cos(pi / 4)
                self.rect.y += self.v * sin(pi / 4)
            elif keys[pygame.K_d]:
                self.image = pygame.transform.rotate(Player.image, -135)
                self.rect.x += self.v * cos(pi / 4)
                self.rect.y += self.v * sin(pi / 4)
            else:
                self.image = pygame.transform.rotate(Player.image, 180)
                self.rect.y += self.v

        elif keys[pygame.K_a] and not (keys[pygame.K_w] and keys[pygame.K_s]):
            self.image = pygame.transform.rotate(Player.image, 90)
            self.rect.x += -self.v

        elif keys[pygame.K_d] and not (keys[pygame.K_w] and keys[pygame.K_s]):
            self.image = pygame.transform.rotate(Player.image, -90)
            self.rect.x += self.v
