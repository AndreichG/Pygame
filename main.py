import sys
import time

import pygame
import sqlite3

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
    button = Button(screen, (255, 0, 0), levels, 0.5, 0.5, 0.2, 0.1, text="Play")
    screen.fill((255, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.VIDEORESIZE:
                button.sc_resize()
                screen.fill((255, 255, 255))
            if event.type == pygame.MOUSEBUTTONDOWN:
                button.check(event.pos, event.button)
        button.render()
        pygame.display.flip()
        clock.tick(fps)


def levels():
    buttons = []
    for i in range(5):
        buttons.append(Button(screen, (32, 128, 255), game, 0.15 * i + 0.2, 0.1, 0.1, 0.1, text=f"{i + 1}", id=i + 1))

    screen.fill((255, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.VIDEORESIZE:
                for i in buttons:
                    i.sc_resize()
                screen.fill((255, 255, 255))
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in buttons:
                    i.check(event.pos, event.button)
        for i in buttons:
            i.render()
        pygame.display.flip()
        clock.tick(fps)


def game(lvl):
    all_sprites = pygame.sprite.Group()
    grid = Grid(screen, (64, 64), 128)
    player = Player(screen, grid, all_sprites)

    con = sqlite3.connect("db\levels.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM lvl{lvl}""").fetchall()

    for elem in result:
        if elem[1] == "laser":
            LaserCannon(screen, grid, (elem[2], elem[3]), elem[4], player, all_sprites)
    con.close()

    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.VIDEORESIZE:
                player.sc_resize()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    levels()
        grid.render()
        #pygame.draw.rect(screen, (255, 0, 0), (screen.get_width() / 5, screen.get_height() / 5, screen.get_width() / 5 * 3, screen.get_height() / 5 * 3), 2)
        #pygame.draw.rect(screen, (0, 255, 0), (player.rect.x, player.rect.y, player.rect.width, player.rect.height), 2)
        #pygame.draw.circle(screen, (255, 0, 0), grid.center, 5)
        #Отладка для игрока и сетки

        all_sprites.draw(screen)
        all_sprites.update()
        if not player.alive():
            time.sleep(1)
            menu()
        #pygame.draw.circle(screen, (0, 0, 0), player.rect.center, 5)
        clock.tick(fps)
        pygame.display.flip()


def main():
    menu()


if __name__ == "__main__":
    main()