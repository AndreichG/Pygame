import sys
import time

import pygame
import sqlite3

from cannons import LaserCannon, OldCannon
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
    buttons = [Button(screen, (255, 0, 0), levels, 0.5, 0.35, 0.2, 0.1, text="Play"),
              Button(screen, (255, 0, 0), controls, 0.5, 0.5, 0.2, 0.1, text="Controls"),
              Button(screen, (255, 0, 0), terminate, 0.5, 0.65, 0.2, 0.1, text="Exit")]
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


def levels():
    buttons = []
    for i in range(5):
        buttons.append(Button(screen, (32, 128, 255), game, 0.15 * i + 0.2, 0.1, 0.1, 0.1, text=f"{i + 1}", arg=i + 1))
    buttons.append(Button(screen, (255, 0, 0), menu, 0.15, 0.9, 0.2, 0.1, text="Back"))
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


def controls():
    buttons = [Button(screen, (255, 0, 0), menu, 0.15, 0.9, 0.2, 0.1, text="Back")]
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
        text = pygame.font.Font(None, 50).render('W - Up', True, (0, 0, 0))
        screen.blit(text, (50, 50))
        text = pygame.font.Font(None, 50).render('A - Left', True, (0, 0, 0))
        screen.blit(text, (50, 100))
        text = pygame.font.Font(None, 50).render('S - Down', True, (0, 0, 0))
        screen.blit(text, (50, 150))
        text = pygame.font.Font(None, 50).render('D - Right', True, (0, 0, 0))
        screen.blit(text, (50, 200))
        text = pygame.font.Font(None, 50).render('LMB - Shoot', True, (0, 0, 0))
        screen.blit(text, (50, 250))
        pygame.display.flip()
        clock.tick(fps)


def game(lvl):
    all_sprites = pygame.sprite.Group()
    grid = Grid(screen, (64, 64), 128)
    player = Player(screen, grid, fps, all_sprites)

    con = sqlite3.connect("db\levels.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM lvl{lvl}""").fetchall()

    for elem in result:
        if elem[1] == "laser":
            LaserCannon(screen, grid, (elem[2], elem[3]), elem[4], player, all_sprites)
        if elem[1] == "old":
            OldCannon(screen, grid, [elem[2], elem[3]], elem[4], player, all_sprites)
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
        #pygame.draw.rect(screen, (255, 0, 0), (screen.get_width() / 5, screen.get_height() / 5, screen.get_width() / 5 * 3, screen.get_height() / 5 * 3), 2)
        #pygame.draw.rect(screen, (0, 255, 0), (player.rect.x, player.rect.y, player.rect.width, player.rect.height), 2)
        #pygame.draw.circle(screen, (255, 0, 0), grid.center, 5)
        #Отладка для игрока и сетки

        grid.render()
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
