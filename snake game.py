import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 205, 50)
RED = (255, 0, 0)
BLUE = (30, 144, 255)
DARK_GREEN = (0, 100, 0)
GRAY = (40, 40, 40)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0
        self.grow_to = 3  # Initial length
        self.is_alive = True
        
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        # Prevent snake from turning directly back on itself
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    
    def move(self):
        if not self.is_alive:
            return
            
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Check for collision with self
        if new_position in self.positions[1:]:
            self.is_alive = False
            return
            
        self.positions.insert(0, new_position)
        
        # Grow snake if needed
        if len(self.positions) > self.grow_to:
            self.positions.pop()
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            # Draw snake segment
            rect = pygame.Rect(p[0] * GRID_SIZE, p[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            
            # Head is a different color
            if i == 0:
                pygame.draw.rect(surface, BLUE, rect)
                pygame.draw.rect(surface, WHITE, rect, 1)
                
                # Draw eyes on head
                eye_size = GRID_SIZE // 5
                # Left eye
                if self.direction == RIGHT:
                    eye_pos = (p[0] * GRID_SIZE + GRID_SIZE - eye_size - 2, p[1] * GRID_SIZE + 5)
                elif self.direction == LEFT:
                    eye_pos = (p[0] * GRID_SIZE + 2, p[1] * GRID_SIZE + 5)
                elif self.direction == UP:
                    eye_pos = (p[0] * GRID_SIZE + 5, p[1] * GRID_SIZE + 2)
                else:  # DOWN
                    eye_pos = (p[0] * GRID_SIZE + 5, p[1] * GRID_SIZE + GRID_SIZE - eye_size - 2)
                
                pygame.draw.rect(surface, WHITE, (eye_pos[0], eye_pos[1], eye_size, eye_size))
                
                # Right eye (offset from left)
                if self.direction == RIGHT:
                    eye_pos = (p[0] * GRID_SIZE + GRID_SIZE - eye_size - 2, p[1] * GRID_SIZE + GRID_SIZE - 5 - eye_size)
                elif self.direction == LEFT:
                    eye_pos = (p[0] * GRID_SIZE + 2, p[1] * GRID_SIZE + GRID_SIZE - 5 - eye_size)
                elif self.direction == UP:
                    eye_pos = (p[0] * GRID_SIZE + GRID_SIZE - 5 - eye_size, p[1] * GRID_SIZE + 2)
                else:  # DOWN
                    eye_pos = (p[0] * GRID_SIZE + GRID_SIZE - 5 - eye_size, p[1] * GRID_SIZE + GRID_SIZE - eye_size - 2)
                
                pygame.draw.rect(surface, WHITE, (eye_pos[0], eye_pos[1], eye_size, eye_size))
            else:
                # Body segments with gradient
                color_intensity = max(50, 255 - i * 3)
                segment_color = (0, color_intensity, 0)
                pygame.draw.rect(surface, segment_color, rect)
                pygame.draw.rect(surface, DARK_GREEN, rect, 1)
    
    def grow(self):
        self.grow_to += 1
        self.score += 10

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)
        
        # Draw a little highlight on the food
        highlight = pygame.Rect(
            self.position[0] * GRID_SIZE + GRID_SIZE // 4,
            self.position[1] * GRID_SIZE + GRID_SIZE // 4,
            GRID_SIZE // 4,
            GRID_SIZE // 4
        )
        pygame.draw.ellipse(surface, (255, 200, 200), highlight)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 25)
        self.big_font = pygame.font.SysFont('Arial', 50, bold=True)
        self.snake = Snake()
        self.food = Food()
        self.speed = FPS
        self.game_over = False
        
    def draw_grid(self):
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH, y), 1)
    
    def draw_score(self):
        score_text = self.font.render(f"Score: {self.snake.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        length_text = self.font.render(f"Length: {self.snake.grow_to}", True, WHITE)
        self.screen.blit(length_text, (WIDTH - 120, 10))
    
    def draw_game_over(self):
        game_over_surface = self.big_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        self.screen.blit(game_over_surface, game_over_rect)
        
        score_surface = self.font.render(f"Final Score: {self.snake.score}", True, WHITE)
        score_rect = score_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
        self.screen.blit(score_surface, score_rect)
        
        restart_surface = self.font.render("Press SPACE to restart or ESC to quit", True, WHITE)
        restart_rect = restart_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        self.screen.blit(restart_surface, restart_rect)
    
    def check_food_collision(self):
        if self.snake.get_head_position() == self.food.position:
            self.snake.grow()
            self.food.randomize_position()
            
            # Make sure food doesn't appear on snake
            while self.food.position in self.snake.positions:
                self.food.randomize_position()
            
            # Slightly increase speed every 5 foods
            if self.snake.score % 50 == 0:
                self.speed += 1
    
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                else:
                    if event.key == pygame.K_UP:
                        self.snake.turn(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.turn(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.turn(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.turn(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
    
    def reset_game(self):
        self.snake.reset()
        self.food.randomize_position()
        self.game_over = False
        self.speed = FPS
        
        # Make sure food doesn't appear on snake
        while self.food.position in self.snake.positions:
            self.food.randomize_position()
    
    def run(self):
        while True:
            self.handle_keys()
            
            if not self.game_over:
                self.snake.move()
                self.check_food_collision()
                
                if not self.snake.is_alive:
                    self.game_over = True
            
            # Draw everything
            self.screen.fill(BLACK)
            self.draw_grid()
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.draw_score()
            
            if self.game_over:
                self.draw_game_over()
            
            pygame.display.update()
            self.clock.tick(self.speed)

if __name__ == "__main__":
    game = Game()
    game.run()