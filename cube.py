import pygame


class Cube:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    length = 0
    rows = 20
    width = 500

    def __init__(self, position, direction, x_dir=1, y_dir=0, color=(255, 0, 0)):
        self.position = position
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.color = color
        self.direction = direction

    def move(self, x_dir, y_dir, direction):
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.direction = direction
        x, y = self.position
        self.position = (x + self.x_dir, y + self.y_dir)

    def draw(self, window, eyes=False):
        distance = self.width // self.rows
        i = self.position[0]
        j = self.position[1]

        pygame.draw.rect(window, self.color, (i * distance + 1, j * distance + 1, distance - 2, distance - 2))

        if eyes:
            centre = distance // 2
            radius = 3
            circle_middle = (i * distance + centre - radius, j * distance + 8)
            circle_middle2 = (i * distance + distance - radius * 2, j * distance + 8)
            pygame.draw.circle(window, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(window, (0, 0, 0), circle_middle2, radius)
