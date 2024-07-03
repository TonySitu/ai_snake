import pygame
import os
import random


WIDTH = 500
HEIGHT = 500
ROWS_COLS = 20


class Snake:
    def __init__(self):
        pass

    def move(self):
        pass

    def draw(self):
        pass


def draw_grid(window):
    size_between = WIDTH // ROWS_COLS

    x = 0
    y = 0
    for i in range(ROWS_COLS):
        x += size_between
        y += size_between

        pygame.draw.line(window, (255, 255, 255), (x, 0), (x, WIDTH))
        pygame.draw.line(window, (255, 255, 255), (0, y), (WIDTH, y))


def draw_window(window):
    window.fill((0, 0, 0))
    draw_grid(window)
    pygame.display.update()


def game_loop(window):
    clock = pygame.time.Clock()
    while True:
        pygame.time.delay(50)
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        draw_window(window)


def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    #snake = Snake((255, 0, 0), (10, 10))

    game_loop(window)


if __name__ == "__main__":
    main()
