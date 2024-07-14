import os
import pygame
import random
import neat
from snake import Snake
from cube import Cube

WIDTH = 500
HEIGHT = 500
ROWS_COLS = 20


def check_collision(snakes, nets, ge):
    snake = snakes[0]
    if len(snake.body) == 1:
        pass
    else:
        for x in range(len(snake.body) - 1):
            if snake.body[x].position in list(map(lambda z: z.position, snake.body[x + 1:])):
                ge[0].fitness -= 1
                snakes.pop(0)
                nets.pop(0)
                ge.pop(0)


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


def game_loop(genomes, config):
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    snake = Snake((255, 0, 0), (5, 5))
    clock = pygame.time.Clock()
    snack = Cube(spawn_snack(snake), snake.direction, color=(0, 255, 0))
    nets = []
    ge = []
    snakes = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        snakes.append(Snake((255, 0, 0), (5, 5)))
        g.fitness = 0
        ge.append(g)

    while len(snakes) > 0:
        clock.tick(10)
        positions = [cube.position for cube in snakes[0].body]
        output = nets[0].activate((snakes[0].head.position, positions, snack.position))
        for i in range(0, 3):
            if max(output) == output[i]:
                if i == 0:
                    snakes[0].move_up()
                elif i == 1:
                    snakes[0].move_down()
                elif i == 2:  # Left
                    snakes[0].move_left()
                else:
                    snakes[0].move_right()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        check_collision(snakes, nets, ge)
        snake.move()
        if snake.body[0].position == snack.position:
            snake.add_cube()
            snack = Cube(spawn_snack(snake), None, color=(0, 255, 0))
            ge[0].fitness += 3

        draw_window(window, snake, snack)


def simulate_run(config_path):
    configuration = neat.config.Config(neat.DefaultGenome,
                                       neat.DefaultReproduction,
                                       neat.DefaultSpeciesSet,
                                       neat.DefaultStagnation,
                                       config_path)
    population = neat.Population(configuration)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    population.run(lambda genomes, config: game_loop(genomes, config), 1)


def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    simulate_run(config_path)


if __name__ == "__main__":
    main()
