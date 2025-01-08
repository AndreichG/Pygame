import pygame


class Grid():
    def __init__(self, screen, size, cell_size):
        self.screen = screen
        self.screen_size = (screen.get_width(), screen.get_height())
        self.center = [screen.get_width() / 2, screen.get_height() / 2]
        self.size = size
        self.cell_size = cell_size

    def render(self):
        w = self.size[0] * self.cell_size
        h = self.size[1] * self.cell_size
        x = self.center[0]
        y = self.center[1]
        for i in range(self.size[0] + 1):
            pygame.draw.line(self.screen, (0, 0, 0),
                             (x - w / 2 + i * self.cell_size,
                              y - h / 2),
                             (x - w / 2 + i * self.cell_size,
                              y + h / 2))
        for i in range(self.size[0] + 1):
            pygame.draw.line(self.screen, (0, 0, 0),
                             (x - w / 2,
                              y - h / 2 + i * self.cell_size),
                             (x + w / 2,
                              y - h / 2 + i * self.cell_size))

    def move(self, d):
        self.center[0] -= d[0]
        self.center[1] -= d[1]