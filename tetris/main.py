import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PALEGREEN = (152, 251, 152)

# Определение размеров экрана и клетки
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
BLOCK_SIZE = 20
MENU_WIDTH = 160

# Создание игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH + MENU_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Загрузка изображений кнопок
pause_img = pygame.image.load('pause.png')
play_img = pygame.image.load('play.png')
stop_img = pygame.image.load('stop.png')
close_img = pygame.image.load('close.png')
reset_img = pygame.image.load('reset.png')

# Определение форм блоков
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

# Функция отрисовки блока
def draw_block(x, y, color):
    pygame.draw.rect(screen, color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, WHITE, (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)

# Функция отрисовки клетчатого фона
def draw_grid():
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

# Класс блока
class Block(object):
    def __init__(self, x, y, shape, block_type):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = self.get_color(block_type)

    def get_color(self, block_type):
        colors = [BLACK, RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE]
        return colors[block_type - 1]

    def draw(self):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col]:
                    draw_block(self.x + col * BLOCK_SIZE, self.y + row * BLOCK_SIZE, self.color)

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]  # Поворот фигуры по часовой стрелке

# Класс игры
class Tetris(object):
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        self.grid = [[0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.block = self.new_block()
        self.next_block = self.new_block()
        self.game_over = False
        self.score = 0
        self.paused = False   

    def new_block(self):
        shape = random.choice(tetris_shapes)
        return Block(SCREEN_WIDTH // 2 - BLOCK_SIZE * len(shape[0]) // 2, 0, shape, random.randint(1, len(tetris_shapes)))

    def check_collision(self):
        for row in range(len(self.block.shape)):
            for col in range(len(self.block.shape[row])):
                if self.block.shape[row][col]:
                    if (self.block.y // BLOCK_SIZE + row >= len(self.grid) or
                            self.block.x // BLOCK_SIZE + col >= len(self.grid[0]) or
                            self.block.x // BLOCK_SIZE + col < 0 or
                            self.grid[self.block.y // BLOCK_SIZE + row][self.block.x // BLOCK_SIZE + col]):
                        return True
        return False

    def update(self):
        if not self.game_over and not self.paused:
            self.block.y += BLOCK_SIZE
            if self.check_collision():
                self.block.y -= BLOCK_SIZE
                self.freeze()
                self.block = self.next_block
                self.next_block = self.new_block()
                self.check_game_over()
                self.clear_lines()

    def check_game_over(self):
        for col in range(len(self.grid[0])):
            if self.grid[0][col]:
                self.game_over = True

    def freeze(self):
        for row in range(len(self.block.shape)):
            for col in range(len(self.block.shape[row])):
                if self.block.shape[row][col]:
                    self.grid[self.block.y // BLOCK_SIZE + row][self.block.x // BLOCK_SIZE + col] = self.block.shape[row][col]

    def clear_lines(self):
        lines_cleared = 0
        for row in range(len(self.grid)):
            if all(self.grid[row]):
                del self.grid[row]
                self.grid.insert(0, [0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)])
                lines_cleared += 1
        self.score += lines_cleared * 100

    def draw(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col]:
                    draw_block(col * BLOCK_SIZE, row * BLOCK_SIZE, self.get_color(self.grid[row][col]))
        self.block.draw()

        # Отображение счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH + 10, 10))

        # Отображение следующей фигуры
        font = pygame.font.Font(None, 36)
        next_text = font.render("Next:", True, BLACK)
        screen.blit(next_text, (SCREEN_WIDTH + 10, 100))
        self.draw_next_block()

        # Отображение кнопок
        if self.paused:
            screen.blit(play_img, self.pause_button_rect)
        else:
            screen.blit(pause_img, self.pause_button_rect)
        screen.blit(stop_img, self.stop_button_rect)
        screen.blit(close_img, self.close_button_rect)
        screen.blit(reset_img, self.reset_button_rect)


        # Отображение "Game Over"
        if self.game_over:
            font = pygame.font.Font(None, 60)
            game_over_text = font.render("Game Over", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
            score_text = font.render(f"Score: {self.score}", True, BLACK)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height()))
        
        


    def draw_next_block(self):
        for row in range(len(self.next_block.shape)):
            for col in range(len(self.next_block.shape[row])):
                if self.next_block.shape[row][col]:
                    draw_block(SCREEN_WIDTH + 10 + col * BLOCK_SIZE, 140 + row * BLOCK_SIZE, self.next_block.color)

    def get_color(self, shape):
        colors = [BLACK, RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW, ORANGE]
        return colors[shape - 1]

    def toggle_pause(self):
        if(self.game_over==False):
            self.paused = not self.paused

    def stop_game(self):
        self.game_over = True

# Главный цикл игры
def main():
    clock = pygame.time.Clock()
    game_over = False
    tetris = Tetris()

    # Определение прямоугольников для кнопок
    tetris.pause_button_rect = pygame.Rect(SCREEN_WIDTH + 10, 200, 50, 50)
    tetris.stop_button_rect = pygame.Rect(SCREEN_WIDTH + 70, 200, 50, 50)
    tetris.close_button_rect = pygame.Rect(SCREEN_WIDTH + 10, 260, 50, 50)
    tetris.reset_button_rect = pygame.Rect(SCREEN_WIDTH + 70, 260, 50, 50)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if not tetris.paused and not tetris.game_over:  # Обработка клавиш только если игра не на паузе и не завершена
                    if event.key == pygame.K_LEFT:
                        tetris.block.x -= BLOCK_SIZE
                        if tetris.check_collision():
                            tetris.block.x += BLOCK_SIZE
                    elif event.key == pygame.K_RIGHT:
                        tetris.block.x += BLOCK_SIZE
                        if tetris.check_collision():
                            tetris.block.x -= BLOCK_SIZE
                    elif event.key == pygame.K_DOWN:
                        tetris.block.y += BLOCK_SIZE
                        if tetris.check_collision():
                            tetris.block.y -= BLOCK_SIZE
                    elif event.key == pygame.K_UP:
                        tetris.block.rotate()
                        if tetris.check_collision():
                            tetris.block.rotate()  # Вернуть фигуру в исходное положение, если поворот невозможен
                if event.key == pygame.K_SPACE:
                    tetris.toggle_pause()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if tetris.pause_button_rect.collidepoint(event.pos):
                    tetris.toggle_pause()
                elif tetris.stop_button_rect.collidepoint(event.pos):
                    tetris.stop_game()
                elif tetris.close_button_rect.collidepoint(event.pos):
                    game_over = True
                elif tetris.reset_button_rect.collidepoint(event.pos):
                    tetris.reset_game()

        screen.fill(PALEGREEN)
        draw_grid()  # Рисуем клетчатый фон
        tetris.update()
        tetris.draw()
        pygame.display.flip()
        clock.tick(5)

    pygame.quit()

if __name__ == "__main__":
    main()
