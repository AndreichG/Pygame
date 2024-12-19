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

class Player(pygame.sprite.Sprite):
    image = load_image("player1.png")

    def __init__(self, screen, *group):
        super().__init__(*group)
        self.image = Player.image
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width() / 2, screen.get_height() / 2)



