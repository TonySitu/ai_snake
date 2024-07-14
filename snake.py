from cube import Cube


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
