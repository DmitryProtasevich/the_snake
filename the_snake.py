from random import randint, choice
import pygame as pg


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BUTTON = {
    (UP, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_LEFT): LEFT,
    (DOWN, pg.K_RIGHT): RIGHT,
    (LEFT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_UP): UP,
    (RIGHT, pg.K_DOWN): DOWN,
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)


BORDER_COLOR = (93, 216, 228)


APPLE_COLOR = (255, 0, 0)


SNAKE_COLOR = (0, 255, 0)


SPEED = 5


screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


pg.display.set_caption(
    'Змейка. Выход - "Esc". Увеличить/уменьшить скорость - "q/a".'
)


clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None) -> None:
        """Инициализация объекта с начальной позицией и цветом."""
        self.position = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Отображение объекта на экране."""
        raise NotImplementedError(
            'Метод draw должен быть переопределён в каждом классе.'
        )

    def draw_rect(self, position, body_color, border_color=None):
        """Рисует прямоугольники"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        if border_color:
            pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self, body_color=APPLE_COLOR, occupied_cells=None):
        """Инициализация яблока и его случайное размещение."""
        if occupied_cells is None:
            occupied_cells = []
        super().__init__(body_color)
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells):
        """
        Случайное положение яблока.
        Ограничил генерацию
        яблока в занимаемой змейкой клетке.
        """
        while True:
            self.position = (
                (randint(0, SCREEN_WIDTH) // GRID_SIZE) * GRID_SIZE,
                (randint(0, SCREEN_HEIGHT) // GRID_SIZE) * GRID_SIZE
            )
            if self.position not in occupied_cells:
                break

    def draw(self):
        """Рисует яблоко"""
        self.draw_rect(self.position, self.body_color, BORDER_COLOR)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализация змейки с начальной позицией, длиной, направлением."""
        super().__init__(body_color)
        self.reset()
        self.last = self.positions[-1]

    def draw(self):
        """Отображает змейку на экране."""
        self.draw_rect(self.get_head_position(), self.body_color, BORDER_COLOR)
        if self.last:
            self.draw_rect(self.last, BOARD_BACKGROUND_COLOR)

    def move(self):
        """Двигает змейку в заданном направлении."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        direction_x = (head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH
        direction_y = (head_y + (direction_y * GRID_SIZE)) % SCREEN_HEIGHT
        return (direction_x, direction_y)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает состояние змейки на начальные параметры."""
        self.positions = [(self.position)]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    global SPEED
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()

                return False
            elif event.key == pg.K_q:
                SPEED += 2
            elif event.key == pg.K_a:
                SPEED -= 2 if SPEED > 2 else 0
            game_object.direction = BUTTON.get(
                (game_object.direction, event.key), game_object.direction)
    return True


def main():
    """Основная функция, запускающая игру."""
    pg.init()
    snake = Snake()
    apple = Apple(occupied_cells=snake.positions)

    while True:
        clock.tick(SPEED)
        if not handle_keys(snake):
            break
        snake.position = snake.move()
        snake.last = snake.positions[-1]
        if snake.position in snake.positions:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)
        else:
            snake.positions.insert(0, snake.position)
            if snake.position == apple.position:
                snake.length += 1
                apple.randomize_position(snake.positions)
            if len(snake.positions) > snake.length:
                snake.positions.pop()
            else:
                None

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
