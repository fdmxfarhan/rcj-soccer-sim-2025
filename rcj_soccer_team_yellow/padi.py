import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 20
GRID_COUNT = WINDOW_SIZE // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (240, 240, 240)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.positions = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = (1, 0)  # Start moving right
        self.grow = False

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        head = self.get_head_position()
        x, y = self.direction
        new_head = ((head[0] + x) % GRID_COUNT, (head[1] + y) % GRID_COUNT)
        
        if new_head in self.positions[1:]:
            return False  # Game over
        
        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        return True

    def draw(self, surface):
        for position in self.positions:
            rect = pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, GREEN, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_COUNT - 1), random.randint(0, GRID_COUNT - 1))

    def draw(self, surface):
        center_x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
        center_y = self.position[1] * GRID_SIZE + GRID_SIZE // 2
        pygame.draw.circle(surface, RED, (center_x, center_y), GRID_SIZE // 2)
        pygame.draw.circle(surface, BLACK, (center_x, center_y), GRID_SIZE // 2, 1)

def main():
    snake = Snake()
    food = Food()
    score = 0
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)

        if not snake.update():
            break

        if snake.get_head_position() == food.position:
            snake.grow = True
            food.randomize_position()
            score += 1

        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        
        # Draw score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.update()
        clock.tick(FPS)

    # Game over screen
    game_over_text = font.render('Game Over!', True, WHITE)
    screen.blit(game_over_text, (WINDOW_SIZE // 2 - 100, WINDOW_SIZE // 2 - 18))
    pygame.display.update()
    pygame.time.wait(2000)

if __name__ == '__main__':
    main()