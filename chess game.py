import pygame
import sys
from typing import List, Tuple, Optional, Dict

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
LIGHT_BROWN = (222, 184, 135)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess Game')

# Load images (would need actual image files in a real implementation)
# For this example, we'll use colored circles as placeholders

class Piece:
    def __init__(self, color: str, row: int, col: int):
        self.color = color  # 'white' or 'black'
        self.row = row
        self.col = col
        self.x = 0
        self.y = 0
        self.calc_pos()
        self.has_moved = False

    def calc_pos(self):
        self.x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

    def move(self, row: int, col: int):
        self.row = row
        self.col = col
        self.calc_pos()
        self.has_moved = True

    def draw(self, screen):
        # Draw a circle as a placeholder for the piece
        radius = SQUARE_SIZE // 2 - 10
        pygame.draw.circle(screen, WHITE if self.color == 'white' else BLACK, (self.x, self.y), radius)
        
        # Draw a smaller circle inside to show the piece type (simplified)
        inner_radius = radius - 10
        pygame.draw.circle(screen, BROWN if self.color == 'white' else LIGHT_BROWN, (self.x, self.y), inner_radius)

    def get_valid_moves(self, board) -> List[Tuple[int, int]]:
        return []

    def __repr__(self):
        return f"{self.color} {self.__class__.__name__} at ({self.row}, {self.col})"


class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.direction = -1 if color == 'white' else 1
        self.en_passant = False

    def draw(self, screen):
        super().draw(screen)
        # Draw a 'P' to indicate pawn
        font = pygame.font.SysFont('Arial', 20)
        text = font.render('P', True, RED if self.color == 'white' else BLUE)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

    def get_valid_moves(self, board) -> List[Tuple[int, int]]:
        moves = []
        
        # Move forward
        if 0 <= self.row + self.direction < ROWS:
            if board[self.row + self.direction][self.col] is None:
                moves.append((self.row + self.direction, self.col))
                
                # Double move from starting position
                if not self.has_moved and board[self.row + 2 * self.direction][self.col] is None:
                    moves.append((self.row + 2 * self.direction, self.col))
        
        # Capture diagonally
        for dc in [-1, 1]:
            if 0 <= self.col + dc < COLS and 0 <= self.row + self.direction < ROWS:
                target = board[self.row + self.direction][self.col + dc]
                if target is not None and target.color != self.color:
                    moves.append((self.row + self.direction, self.col + dc))
        
        # TODO: Implement en passant
        
        return moves


class Rook(Piece):
    def draw(self, screen):
        super().draw(screen)
        # Draw a 'R' to indicate rook
        font = pygame.font.SysFont('Arial', 20)
        text = font.render('R', True, RED if self.color == 'white' else BLUE)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

    def get_valid_moves(self, board) -> List[Tuple[int, int]]:
        moves = []
        
        # Horizontal and vertical moves
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                r, c = self.row + dr * i, self.col + dc * i
                if 0 <= r < ROWS and 0 <= c < COLS:
                    target = board[r][c]
                    if target is None:
                        moves.append((r, c))
                    else:
                        if target.color != self.color:
                            moves.append((r, c))
                        break
                else:
                    break
        
        return moves


class Knight(Piece):
    def draw(self, screen):
        super().draw(screen)
        # Draw a 'N' to indicate knight
        font = pygame.font.SysFont('Arial', 20)
        text = font.render('N', True, RED if self.color == 'white' else BLUE)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

    def get_valid_moves(self, board) -> List[Tuple[int, int]]:
        moves = []
        knight_moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]
        
        for dr, dc in knight_moves:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        
        return moves


class Bishop(Piece):
    def draw(self, screen):
        super().draw(screen)
        # Draw a 'B' to indicate bishop
        font = pygame.font.SysFont('Arial', 20)
        text = font.render('B', True, RED if self.color == 'white' else BLUE)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

    def get_valid_moves(self, board) -> List[Tuple[int, int]]:
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                r, c = self.row + dr * i, self.col + dc * i
                if 0 <= r < ROWS and 0 <= c < COLS:
                    target = board[r][c]
                    if target is None:
                        moves.append((r, c))
                    else:
                        if target.color != self.color:
                            moves.append((r, c))
                        break
                else:
                    break
        
        return moves


class Queen(Piece):
    def draw(self, screen):
        super().draw(screen)
        # Draw a 'Q' to indicate queen
        font = pygame.font.SysFont('Arial', 20)
        text = font.render('Q', True, RED if self.color == 'white' else BLUE)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

    def get_valid_moves(self, board) -> List[Tuple[int, int]]:
        # Combine rook and bishop moves
        rook_moves = Rook(self.color, self.row, self.col).get_valid_moves(board)
        bishop_moves = Bishop(self.color, self.row, self.col).get_valid_moves(board)
        return rook_moves + bishop_moves


class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.in_check = False

    def draw(self, screen):
        super().draw(screen)
        # Draw a 'K' to indicate king
        font = pygame.font.SysFont('Arial', 20)
        text = font.render('K', True, RED if self.color == 'white' else BLUE)
        text_rect = text.get_rect(center=(self.x, self.y))
        screen.blit(text, text_rect)

    def get_valid_moves(self, board) -> List[Tuple[int, int]]:
        moves = []
        king_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        
        for dr, dc in king_moves:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        
        # TODO: Implement castling
        
        return moves


class ChessGame:
    def __init__(self):
        self.board = self.create_board()
        self.turn = 'white'
        self.selected_piece = None
        self.valid_moves = []
        self.white_king = self.board[7][4]
        self.black_king = self.board[0][4]
        self.game_over = False
        self.winner = None

    def create_board(self) -> List[List[Optional[Piece]]]:
        board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        
        # Create pawns
        for col in range(COLS):
            board[1][col] = Pawn('black', 1, col)
            board[6][col] = Pawn('white', 6, col)
        
        # Create rooks
        board[0][0] = Rook('black', 0, 0)
        board[0][7] = Rook('black', 0, 7)
        board[7][0] = Rook('white', 7, 0)
        board[7][7] = Rook('white', 7, 7)
        
        # Create knights
        board[0][1] = Knight('black', 0, 1)
        board[0][6] = Knight('black', 0, 6)
        board[7][1] = Knight('white', 7, 1)
        board[7][6] = Knight('white', 7, 6)
        
        # Create bishops
        board[0][2] = Bishop('black', 0, 2)
        board[0][5] = Bishop('black', 0, 5)
        board[7][2] = Bishop('white', 7, 2)
        board[7][5] = Bishop('white', 7, 5)
        
        # Create queens
        board[0][3] = Queen('black', 0, 3)
        board[7][3] = Queen('white', 7, 3)
        
        # Create kings
        board[0][4] = King('black', 0, 4)
        board[7][4] = King('white', 7, 4)
        
        return board

    def draw_board(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                color = LIGHT_BROWN if (row + col) % 2 == 0 else BROWN
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                # Highlight selected piece
                if self.selected_piece and self.selected_piece.row == row and self.selected_piece.col == col:
                    pygame.draw.rect(screen, BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
                
                # Highlight valid moves
                if (row, col) in self.valid_moves:
                    pygame.draw.rect(screen, GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

    def draw_pieces(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece:
                    piece.draw(screen)

    def select_piece(self, row: int, col: int) -> bool:
        piece = self.board[row][col]
        if piece and piece.color == self.turn:
            self.selected_piece = piece
            self.valid_moves = piece.get_valid_moves(self.board)
            return True
        return False

    def move_piece(self, row: int, col: int) -> bool:
        if self.selected_piece and (row, col) in self.valid_moves:
            # Capture the piece if it exists
            if self.board[row][col]:
                captured_piece = self.board[row][col]
                # Check if capturing the king
                if isinstance(captured_piece, King):
                    self.game_over = True
                    self.winner = self.turn
            
            # Move the piece
            self.board[self.selected_piece.row][self.selected_piece.col] = None
            self.board[row][col] = self.selected_piece
            self.selected_piece.move(row, col)
            
            # Check for pawn promotion
            if isinstance(self.selected_piece, Pawn) and (row == 0 or row == 7):
                self.board[row][col] = Queen(self.selected_piece.color, row, col)
            
            self.change_turn()
            self.selected_piece = None
            self.valid_moves = []
            return True
        return False

    def change_turn(self):
        self.turn = 'black' if self.turn == 'white' else 'white'

    def is_in_check(self, color: str) -> bool:
        king = self.white_king if color == 'white' else self.black_king
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece and piece.color != color:
                    if (king.row, king.col) in piece.get_valid_moves(self.board):
                        return True
        return False

    def draw_game_over(self, screen):
        if self.game_over:
            font = pygame.font.SysFont('Arial', 50)
            text = font.render(f"{self.winner.capitalize()} wins!", True, RED)
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(text, text_rect)

    def update(self):
        # Update king references (in case they moved)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if isinstance(piece, King):
                    if piece.color == 'white':
                        self.white_king = piece
                    else:
                        self.black_king = piece


def main():
    game = ChessGame()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if not game.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE
                
                if game.selected_piece:
                    if not game.move_piece(row, col):
                        game.select_piece(row, col)
                else:
                    game.select_piece(row, col)
        
        game.update()
        game.draw_board(screen)
        game.draw_pieces(screen)
        game.draw_game_over(screen)
        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()