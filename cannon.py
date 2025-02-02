import pygame


class Cannon(pygame.sprite.Sprite):
    def __init__(self, screen, grid, pos, direction, can_rotate, player, *group):
        self.screen = screen
        self.grid = grid
        self.pos = pos
        self.direction = direction
        self.player = player
        super().__init__(*group)
        self.can_rotate = can_rotate

    def place(self):
        x = self.grid.center[0] + self.pos[0] * self.grid.cell_size
        y = self.grid.center[1] + self.pos[1] * self.grid.cell_size
        return x, y

    def on_screen(self, x, y):
        xp, yp = 0, 0
        if x < 0 or x > self.screen.get_width() or y < 0 or y > self.screen.get_height():
            if x < 0:
                xp = 10
            elif x > self.screen.get_width():
                xp = self.screen.get_width() - 10
            else:
                xp = x
            if y < 0:
                yp = 10
            elif y > self.screen.get_height():
                yp = self.screen.get_height() - 10
            else:
                yp = y
            pygame.draw.circle(self.screen, (220, 0, 0), (xp, yp), 8)
