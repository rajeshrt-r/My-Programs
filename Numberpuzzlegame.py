import pygame
import sys
import random
from typing import List, Tuple, Optional

# Initialize pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 4
TILE_SIZE = WINDOW_SIZE // GRID_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 120, 255)
GREEN = (0, 200, 100)
RED = (255, 50, 50)

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('15-Puzzle Game')
clock = pygame.time.Clock()

class Puzzle:
    def __init__(self):
        self.tiles = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.empty_pos = (GRID_SIZE - 1, GRID_SIZE - 1)  # Bottom-right corner
        self.moves = 0
        self.solved = False
        self.font = pygame.font.SysFont('Arial', TILE_SIZE // 3)
        self.initialize_puzzle()

    def initialize_puzzle(self):
        # Create solved puzzle first
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self.tiles[row][col] = row * GRID_SIZE + col + 1
        
        # Set the last tile as empty (0 represents empty)
        self.tiles[GRID_SIZE-1][GRID_SIZE-1] = 0
        
        # Shuffle the puzzle with valid moves
        self.shuffle_puzzle()

    def shuffle_puzzle(self):
        # Make many random valid moves to shuffle
        for _ in range(1000):
            possible_moves = self.get_possible_moves()
            if possible_moves:
                move = random.choice(possible_moves)
                self.move_tile(move)

        self.moves = 0
        self.solved = False

    def get_possible_moves(self) -> List[Tuple[int, int]]:
        moves = []
        empty_row, empty_col = self.empty_pos
        
        # Check adjacent tiles that can move into empty space
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_row, new_col = empty_row + dr, empty_col + dc
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                moves.append((new_row, new_col))
        
        return moves

    def move_tile(self, pos: Tuple[int, int]) -> bool:
        row, col = pos
        empty_row, empty_col = self.empty_pos
        
        # Check if the tile is adjacent to empty space
        if (abs(row - empty_row) == 1 and col == empty_col) or \
           (abs(col - empty_col) == 1 and row == empty_row):
            # Swap tile with empty space
            self.tiles[empty_row][empty_col] = self.tiles[row][col]
            self.tiles[row][col] = 0
            self.empty_pos = (row, col)
            self.moves += 1
            
            # Check if puzzle is solved
            self.check_solved()
            return True
        
        return False

    def check_solved(self):
        # Check if all tiles are in order
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if row == GRID_SIZE - 1 and col == GRID_SIZE - 1:
                    if self.tiles[row][col] != 0:
                        self.solved = False
                        return
                elif self.tiles[row][col] != row * GRID_SIZE + col + 1:
                    self.solved = False
                    return
        
        self.solved = True

    def draw(self, surface):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                value = self.tiles[row][col]
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, 
                                 TILE_SIZE, TILE_SIZE)
                
                if value == 0:  # Empty tile
                    pygame.draw.rect(surface, BLACK, rect)
                else:
                    # Tile background
                    pygame.draw.rect(surface, BLUE, rect)
                    pygame.draw.rect(surface, WHITE, rect, 2)
                    
                    # Tile number
                    text = self.font.render(str(value), True, WHITE)
                    text_rect = text.get_rect(center=rect.center)
                    surface.blit(text, text_rect)
        
        # Draw move counter
        move_text = self.font.render(f"Moves: {self.moves}", True, WHITE)
        surface.blit(move_text, (10, 10))

        # Draw solved message
        if self.solved:
            solved_rect = pygame.Rect(WINDOW_SIZE//4, WINDOW_SIZE//3, 
                                    WINDOW_SIZE//2, WINDOW_SIZE//3)
            pygame.draw.rect(surface, GREEN, solved_rect)
            pygame.draw.rect(surface, WHITE, solved_rect, 3)
            
            solved_text = self.font.render("Solved!", True, WHITE)
            solved_text_rect = solved_text.get_rect(center=solved_rect.center)
            surface.blit(solved_text, solved_text_rect)
            
            restart_text = self.font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(solved_rect.centerx, 
                                                       solved_rect.centery + 50))
            surface.blit(restart_text, restart_rect)

def main():
    puzzle = Puzzle()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart game
                    puzzle.initialize_puzzle()
                
                # Move tiles with arrow keys
                empty_row, empty_col = puzzle.empty_pos
                if event.key == pygame.K_UP and empty_row < GRID_SIZE - 1:
                    puzzle.move_tile((empty_row + 1, empty_col))
                elif event.key == pygame.K_DOWN and empty_row > 0:
                    puzzle.move_tile((empty_row - 1, empty_col))
                elif event.key == pygame.K_LEFT and empty_col < GRID_SIZE - 1:
                    puzzle.move_tile((empty_row, empty_col + 1))
                elif event.key == pygame.K_RIGHT and empty_col > 0:
                    puzzle.move_tile((empty_row, empty_col - 1))
            
            elif event.type == pygame.MOUSEBUTTONDOWN and not puzzle.solved:
                # Get mouse position and convert to grid coordinates
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = mouse_x // TILE_SIZE
                row = mouse_y // TILE_SIZE
                
                # Try to move the clicked tile
                puzzle.move_tile((row, col))

        # Draw everything
        screen.fill(BLACK)
        puzzle.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()