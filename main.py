import sys

import pygame
import sqlite3
import time

from lasercannon import LaserCannon
from mortar import Mortar
from oldcannon import OldCannon
from permalasercannon import PermaLaserCannon
from player import Player
from grid import Grid
from button import Button
from projectiles import Laser, CannonBall, MortarShot, Grenade, PermaLaser


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
               Button(screen, (255, 0, 0), controls, 0.5, 0.65, 0.2, 0.1, text="Controls"),
               Button(screen, (255, 0, 0), terminate, 0.5, 0.8, 0.2, 0.1, text="Exit"),
               Button(screen, (255, 0, 0), stats, 0.5, 0.5, 0.2, 0.1, text="Stats for nerds")]
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


def stats():
    buttons = [Button(screen, (255, 0, 0), menu, 0.15, 0.9, 0.2, 0.1, text="Back")]
    screen.fill((255, 255, 255))
    file = open("db/stats.txt", "r")
    kills = list(map(int, file.readlines()))
    file.close()
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

        text = pygame.font.Font(None, 50).render(f'Laser cannons destroyed: {kills[0]}', True, (0, 0, 0))
        screen.blit(text, (50, 50))
        text = pygame.font.Font(None, 50).render(f'Perma laser cannons destroyed: {kills[1]}', True, (0, 0, 0))
        screen.blit(text, (50, 100))
        text = pygame.font.Font(None, 50).render(f'Old cannons destroyed: {kills[2]}', True, (0, 0, 0))
        screen.blit(text, (50, 150))
        text = pygame.font.Font(None, 50).render(f'Mortars destroyed: {kills[3]}', True, (0, 0, 0))
        screen.blit(text, (50, 200))
        text = pygame.font.Font(None, 50).render(f'All cannons destroyed: {sum(kills)}', True, (0, 0, 0))
        screen.blit(text, (50, 250))
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
        text = pygame.font.Font(None, 50).render('SPACE - Shoot', True, (0, 0, 0))
        screen.blit(text, (50, 250))
        pygame.display.flip()
        clock.tick(fps)


def game_over(lvl):
    buttons = [Button(screen, (255, 0, 0), game, 0.5, 0.35, 0.2, 0.1, text="Retry", arg=lvl),
               Button(screen, (255, 0, 0), levels, 0.5, 0.5, 0.2, 0.1, text="Back")]
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.VIDEORESIZE:
                for i in buttons:
                    i.sc_resize()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in buttons:
                    i.check(event.pos, event.button)
        for i in buttons:
            i.render()
        text = pygame.font.Font(None, 50).render('You died!', True, (0, 0, 0))
        screen.blit(text, (0.5 * screen.get_width() - text.get_width() / 2, 100))
        pygame.display.flip()
        clock.tick(fps)


def win(lvl):
    buttons = [Button(screen, (255, 0, 0), game, 0.5, 0.35, 0.2, 0.1, text="Play again", arg=lvl),
               Button(screen, (255, 0, 0), levels, 0.5, 0.5, 0.2, 0.1, text="Back")]
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.VIDEORESIZE:
                for i in buttons:
                    i.sc_resize()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in buttons:
                    i.check(event.pos, event.button)
        for i in buttons:
            i.render()
        text = pygame.font.Font(None, 50).render('Victory', True, (0, 0, 0))
        screen.blit(text, (0.5 * screen.get_width() - text.get_width() / 2, 100))
        pygame.display.flip()
        clock.tick(fps)



def game(lvl):
    all_sprites = pygame.sprite.Group()
    cannons = pygame.sprite.Group()
    grenades = pygame.sprite.Group()
    grid = Grid(screen, (64, 64), 128)
    player = Player(screen, grid, all_sprites)
    t = 0
    SHOOT = pygame.USEREVENT + 1
    pygame.time.set_timer(SHOOT, 4000)
    con = sqlite3.connect("db\levels.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT * FROM lvl{lvl}""").fetchall()

    for elem in result:
        if elem[1] == "l":
            LaserCannon(screen, grid, [elem[2], elem[3]], elem[4], elem[5], all_sprites, cannons)
        if elem[1] == "o":
            OldCannon(screen, grid, [elem[2], elem[3]], elem[4], elem[5], all_sprites, cannons)
        if elem[1] == "m":
            Mortar(screen, grid, [elem[2], elem[3]], elem[4], elem[5], all_sprites, cannons)
        if elem[1] == "p":
            PermaLaser(screen, grid, [elem[2] + 0.5, elem[3] + 0.5], elem[4], player, PermaLaserCannon(screen, grid, [elem[2], elem[3]], elem[4], elem[5], all_sprites, cannons), all_sprites)

    con.close()

    for i in cannons.sprites():
        if i.__class__ == Mortar:
            MortarShot(screen, grid, [i.pos[0] + 0.5, i.pos[1] + 0.5], i.direction, player, all_sprites)
        if i.__class__ == OldCannon:
            CannonBall(screen, grid, [i.pos[0] + 0.5, i.pos[1] + 0.5], i.direction, player, all_sprites)
        if i.__class__ == LaserCannon:
            Laser(screen, grid, [i.pos[0] + 0.5, i.pos[1] + 0.5], i.direction, player, i, all_sprites)

    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == SHOOT:
                for i in cannons.sprites():
                    if i.__class__ == Mortar:
                        MortarShot(screen, grid, [i.pos[0] + 0.5, i.pos[1] + 0.5], i.direction, player, all_sprites)
                    if i.__class__ == OldCannon:
                        CannonBall(screen, grid, [i.pos[0] + 0.5, i.pos[1] + 0.5], i.direction, player, all_sprites)
                    if i.__class__ == LaserCannon:
                        Laser(screen, grid, [i.pos[0] + 0.5, i.pos[1] + 0.5], i.direction, player, i, all_sprites)
            if event.type == pygame.VIDEORESIZE:
                player.sc_resize()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    levels()
                if event.key == pygame.K_SPACE:
                    t = time.time()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if t != 0 and time.time() - t > 1:
                        Grenade(screen, grid, player.pos, player.direction, all_sprites, grenades)
                    t = 0
        #pygame.draw.rect(screen, (255, 0, 0), (screen.get_width() / 5, screen.get_height() / 5, screen.get_width() / 5 * 3, screen.get_height() / 5 * 3), 2)
        #pygame.draw.rect(screen, (0, 255, 0), (player.rect.x, player.rect.y, player.rect.width, player.rect.height), 2)
        #pygame.draw.circle(screen, (255, 0, 0), grid.center, 5)
        #Отладка для игрока и сетки
        grid.render()
        all_sprites.draw(screen)
        all_sprites.update(fps)
        if t != 0 and time.time() - t > 1:
            pygame.draw.circle(screen, (0, 255, 0), player.rect.center, 5)
        file = open("db/stats.txt", "r")
        kills = list(map(int, file.readlines()))
        file.close()
        for i in cannons.sprites():
            for j in grenades.sprites():
                if pygame.sprite.collide_mask(i, j):
                    if i.__class__ == Mortar:
                        kills[3] += 1
                    if i.__class__ == OldCannon:
                        kills[2] += 1
                    if i.__class__ == LaserCannon:
                        kills[0] += 1
                    if i.__class__ == PermaLaserCannon:
                        kills[1] += 1
                    i.kill()
                    j.kill()
        file = open("db/stats.txt", "w")
        file.write("\n".join(list(map(str, kills))))
        file.close()
        if not cannons.sprites():
            win(lvl)
        if not player.alive():
            game_over(lvl)
        #pygame.draw.circle(screen, (0, 0, 0), player.rect.center, 5)
        clock.tick(fps)
        pygame.display.flip()


def main():
    menu()


if __name__ == "__main__":
    main()
