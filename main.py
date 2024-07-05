import pygame
import random

WIDTH = 500
HEIGHT = 500
ROWS_COLS = 20


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


class Snake:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    body = []
    turns = {}

    def __init__(self, color, position, direction=RIGHT):
        self.color = color
        self.head = Cube(position, direction)
        self.body.append(self.head)
        self.x_dir = 1
        self.y_dir = 0
        self.direction = direction
        self.commands = {
            pygame.K_UP: self.move_up,
            pygame.K_DOWN: self.move_down,
            pygame.K_LEFT: self.move_left,
            pygame.K_RIGHT: self.move_right
        }

    def move_up(self):
        self.x_dir = 0
        self.y_dir = -1
        self.direction = self.UP
        self.turns[self.head.position[:]] = (self.x_dir, self.y_dir, self.direction)

    def move_down(self):
        self.x_dir = 0
        self.y_dir = 1
        self.direction = self.DOWN
        self.turns[self.head.position[:]] = (self.x_dir, self.y_dir, self.direction)

    def move_left(self):
        self.x_dir = -1
        self.y_dir = 0
        self.direction = self.LEFT
        self.turns[self.head.position[:]] = (self.x_dir, self.y_dir, self.direction)

    def move_right(self):
        self.x_dir = 1
        self.y_dir = 0
        self.direction = self.RIGHT
        self.turns[self.head.position[:]] = (self.x_dir, self.y_dir, self.direction)

    def move(self):
        keys = pygame.key.get_pressed()
        for key in self.commands:
            if keys[key]:
                self.commands[key]()

        for index, cube in enumerate(self.body):
            x, y = cube.position
            if (x, y) in self.turns:
                cube.move(*self.turns[(x, y)])
                if index == len(self.body) - 1:
                    self.turns.pop((x, y))
            else:
                if cube.direction == cube.LEFT and x <= 0:
                    cube.position = (ROWS_COLS - 1, y)
                elif cube.direction == cube.RIGHT and x >= ROWS_COLS - 1:
                    cube.position = (0, y)
                elif cube.direction == cube.DOWN and y >= ROWS_COLS - 1:
                    cube.position = (x, 0)
                elif cube.direction == cube.UP and y <= 0:
                    cube.position = (x, ROWS_COLS - 1)
                else:  # only move straight if not at edge
                    cube.move(cube.x_dir, cube.y_dir, cube.direction)

    def draw(self, window):
        for index, cube in enumerate(self.body):
            if index == 0:
                cube.draw(window, True)
            else:
                cube.draw(window)

    def add_cube(self):
        tail = self.body[-1]
        x, y = tail.position

        match tail.direction:
            case 'UP':
                self.body.append(Cube((x, y + 1), tail.direction, tail.x_dir, tail.y_dir))
            case "DOWN":
                self.body.append(Cube((x, y - 1), tail.direction, tail.x_dir, tail.y_dir))
            case "LEFT":
                self.body.append(Cube((x + 1, y), tail.direction, tail.x_dir, tail.y_dir))
            case "RIGHT":
                self.body.append(Cube((x - 1, y), tail.direction, tail.x_dir, tail.y_dir))


def draw_grid(window):
    size_between = WIDTH // ROWS_COLS

    x = 0
    y = 0
    for i in range(ROWS_COLS):
        x += size_between
        y += size_between

        pygame.draw.line(window, (255, 255, 255), (x, 0), (x, WIDTH))
        pygame.draw.line(window, (255, 255, 255), (0, y), (WIDTH, y))


def draw_window(window, snake, snack):
    window.fill((0, 0, 0))
    draw_grid(window)
    snake.draw(window)
    snack.draw(window)
    pygame.display.update()


def spawn_snack(snake):
    positions = snake.body

    while True:
        x = random.randrange(ROWS_COLS)
        y = random.randrange(ROWS_COLS)

        if len(list(filter(lambda z: z.position == (x, y), positions))) > 0:
            continue
        else:
            break

    return x, y


def game_loop():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    snake = Snake((255, 0, 0), (5, 5))
    clock = pygame.time.Clock()
    snack = Cube(spawn_snack(snake), snake.direction, color=(0, 255, 0))

    while True:
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        snake.move()
        if snake.body[0].position == snack.position:
            snake.add_cube()
            snack = Cube(spawn_snack(snake), None, color=(0, 255, 0))

        draw_window(window, snake, snack)


def main():
    game_loop()


if __name__ == "__main__":
    main()
