from random import randint

import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


BOARD_BACKGROUND_COLOR = (0, 0, 0)


BORDER_COLOR = (93, 216, 228)


APPLE_COLOR = (255, 0, 0)


SNAKE_COLOR = (0, 255, 0)


SPEED = 5


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)


pygame.display.set_caption('Змейка')


clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self) -> None:
        """Инициализация объекта с начальной позицией и цветом."""
        self.position = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Отображение объекта на экране."""
        pass


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self):
        """Инициализация яблока и его случайное размещение."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """
        Добавил ограничение, исключающее генерацию
        яблока в занимаемой змейкой клетке.
        """
        while True:
            x = (randint(0, SCREEN_WIDTH) // GRID_SIZE) * GRID_SIZE
            y = (randint(0, SCREEN_HEIGHT) // GRID_SIZE) * GRID_SIZE
            self.position = (x, y)
            if self.position not in Snake().positions:
                break

    def draw(self):
        """Отображает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Инициализация змейки с начальной позицией, длиной, направлением."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [(20, 240)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = self.positions[-1]

    def draw(self):
        """Отображает змейку на экране."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Обновляет направление движения змейки после нажатия клавиш."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple):
        """
        Двигает змейку в заданном направлении, обрабатывает
        столкновения и поедание яблок.
        """
        self.get_head_position()

        if self.direction == RIGHT:
            new_head = (self.head_position[0]
                        + GRID_SIZE, self.head_position[1])
            if new_head[0] >= SCREEN_WIDTH:
                new_head = (0, self.head_position[1])
        elif self.direction == LEFT:
            new_head = (self.head_position[0]
                        - GRID_SIZE, self.head_position[1])
            if new_head[0] < 0:
                new_head = (SCREEN_WIDTH - GRID_SIZE, self.head_position[1])
        elif self.direction == UP:
            new_head = (self.head_position[0],
                        self.head_position[1] - GRID_SIZE)
            if new_head[1] < 0:
                new_head = (self.head_position[0], SCREEN_HEIGHT - GRID_SIZE)
        elif self.direction == DOWN:
            new_head = (self.head_position[0],
                        self.head_position[1] + GRID_SIZE)
            if new_head[1] >= SCREEN_HEIGHT:
                new_head = (self.head_position[0], 0)

        if new_head in self.positions[1:]:
            self.reset()

        self.positions.insert(0, new_head)

        if new_head == apple.position:
            self.length += 1
            apple.randomize_position()
        if len(self.positions) > (self.length + 1):
            self.positions.pop()

        self.draw()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        self.head_position = self.positions[0]
        return self.head_position

    def reset(self):
        """Сбрасывает состояние змейки на начальные параметры."""
        self.positions = [(20, 240)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция, запускающая игру."""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move(apple)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
