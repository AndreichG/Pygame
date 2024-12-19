import pygame
from player import Player


pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
screen.fill((255, 255, 255))
clock = pygame.time.Clock()
fps = 60


def main():
    all_sprites = pygame.sprite.Group()
    player = Player(screen, all_sprites)


    running = True
    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()