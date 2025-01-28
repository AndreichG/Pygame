import sys
import pygame

from cannons import LaserCannon
from player import Player
from grid import Grid
from button import Button


pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
screen.fill((255, 255, 255))
clock = pygame.time.Clock()
fps = 60


def terminate():
    pygame.quit()
    sys.exit()


def menu():
    button = Button(screen, (255, 0, 0), game, 640, 360, 250, 80, text="Play")
    screen.fill((255, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.VIDEORESIZE:
                button.sc_resize()
                screen.fill((255, 255, 255))
        button.update()
        pygame.display.flip()
        clock.tick(fps)


def game():
    all_sprites = pygame.sprite.Group()
    grid = Grid(screen, (64, 64), 128)
    player = Player(screen, grid, all_sprites)
    LaserCannon(screen, grid, (1, 1), 0, player, all_sprites)

    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.VIDEORESIZE:
                player.sc_resize()
        grid.render()
        #pygame.draw.rect(screen, (255, 0, 0), (screen.get_width() / 5, screen.get_height() / 5, screen.get_width() / 5 * 3, screen.get_height() / 5 * 3), 2)
        #pygame.draw.rect(screen, (0, 255, 0), (player.rect.x, player.rect.y, player.rect.width, player.rect.height), 2)
        #pygame.draw.circle(screen, (255, 0, 0), grid.center, 5)
        #Отладка для игрока и сетки

        all_sprites.draw(screen)
        all_sprites.update()
        if not player.alive():
            menu()
        #pygame.draw.circle(screen, (0, 0, 0), player.rect.center, 5)
        clock.tick(fps)
        pygame.display.flip()


if __name__ == "__main__":
    menu()