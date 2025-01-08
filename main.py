import pygame
from player import Player
from grid import Grid


pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
screen.fill((255, 255, 255))
clock = pygame.time.Clock()
fps = 60


def main():
    all_sprites = pygame.sprite.Group()
    grid = Grid(screen, (128, 128), 64)
    player = Player(screen, grid, all_sprites)


    running = True
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                player.sc_resize()
        #grid.render()
        #pygame.draw.rect(screen, (255, 0, 0), (screen.get_width() / 5, screen.get_height() / 5, screen.get_width() / 5 * 3, screen.get_height() / 5 * 3), 2)
        #pygame.draw.rect(screen, (0, 255, 0), (player.rect.x, player.rect.y, player.rect.width, player.rect.height), 2)
        #pygame.draw.circle(screen, (255, 0, 0), grid.center, 5)
        #Отладка для игрока и сетки

        player.move()
        player.check()
        all_sprites.draw(screen)
        pygame.draw.circle(screen, (0, 0, 0), player.rect.center, 5)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()