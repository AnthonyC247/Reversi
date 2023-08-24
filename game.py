import pygame
import sys
import numpy as np
import heapq

class ReversiGame:
    def __init__(self):
        """
        Initialize the Reversi game.
        """
        pygame.init()
        self.size = self.width, self.height = 500, 500
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Reversi/Othello")

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 128, 0)
        self.BLUE = (0, 0, 255)

        self.ROWS = self.COLS = 8
        self.SQUARE_SIZE = self.width // self.COLS
        self.board = np.zeros((self.ROWS, self.COLS))
        self.player = 1
        self.game_over = False

    def draw_board(self):
        """
        Draw the game board with pieces on the screen.
        """
        self.screen.fill(self.GREEN)
        for row in range(self.ROWS):
            for col in range(self.COLS):
                pygame.draw.rect(self.screen, self.BLACK, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
                if self.board[row][col] == 1:
                    pygame.draw.circle(self.screen, self.WHITE, (
                        col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2, row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2), self.SQUARE_SIZE // 2 - 5)
                elif self.board[row][col] == -1:
                    pygame.draw.circle(self.screen, self.BLUE, (
                        col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2, row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2), self.SQUARE_SIZE // 2 - 5)
        pygame.display.update()

    def is_valid_move(self, row, col, player): 
        if self.board[row][col] != 0:
            return False
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for direction in directions:
            if self.is_valid_direction(row, col, player, direction):
                return True
        return False

    def is_valid_direction(self, row, col, player, direction):
        """
        Check if a move in a specific direction is valid for the current player.
        """
        delta_row, delta_col = direction
        current_row, current_col = row + delta_row, col + delta_col
        if not (0 <= current_row < self.ROWS and 0 <= current_col < self.COLS and self.board[current_row][current_col] == -player):
            return False
        flips = []
        while 0 <= current_row < self.ROWS and 0 <= current_col < self.COLS:
            if self.board[current_row][current_col] == 0:
                return False
            elif self.board[current_row][current_col] == player:
                for flip in flips:
                    flip_row, flip_col = flip
                    self.board[flip_row][flip_col] = player
                return True
            flips.append((current_row, current_col))
            current_row += delta_row
            current_col += delta_col
        return False

    def make_move(self, row, col, player):
        """
        Make a move for the current player and update the board accordingly.
        """
        self.board[row][col] = player
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for direction in directions:
            if self.is_valid_direction(row, col, player, direction):
                self.flip_pieces(row, col, player, direction)

    def flip_pieces(self, row, col, player, direction):
        delta_row, delta_col = direction
        current_row, current_col = row + delta_row, col + delta_col
        while self.board[current_row][current_col] == -player:
            self.board[current_row][current_col] = player
            current_row += delta_row
            current_col += delta_col

    def get_valid_moves(self, player):
        """
        Get the list of valid moves for the given player.
        """
        valid_moves = []
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.is_valid_move(row, col, player):
                    valid_moves.append((row, col))
        return valid_moves

    def evaluate_board(self):
        """
        Evaluate the current state (score) of the board.
        """
        score = np.sum(self.board)
        return score

    def minimax(self, depth, maximizing_player):
        # Implementation of the minimax algorithm for AI decision-making.
        if depth == 0:
            return self.evaluate_board()

        valid_moves = self.get_valid_moves(1 if maximizing_player else -1)
        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                row, col = move
                new_board = self.board.copy()
                self.make_move(row, col, 1)
                eval = self.minimax(depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in valid_moves:
                row, col = move
                new_board = self.board.copy()
                self.make_move(row, col, -1)
                eval = self.minimax(depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def get_best_move(self, depth, player):
        valid_moves = self.get_valid_moves(player)
        best_move = None

        if player == 1:
            cmp_func = lambda x, y: y[1] - x[1]  # Max-heap for player 1
        else:
            cmp_func = lambda x, y: x[1] - y[1]  # Min-heap for player -1

        move_heap = []  # Priority queue for storing moves
        for move in valid_moves:
            row, col = move
            new_board = self.board.copy()
            self.make_move(row, col, player)
            eval_score = self.minimax(depth - 1, False)
            heapq.heappush(move_heap, (move, eval_score))

        best_move, _ = heapq.heappop(move_heap)  # Get the best move from the priority queue
        return best_move

    def show_game_over_screen(self):
        font = pygame.font.Font(None, 36)
        if self.evaluate_board() > 0:
            text = font.render("White wins!", True, self.WHITE)
        elif self.evaluate_board() < 0:
            text = font.render("Blue wins!", True, self.BLUE)
        else:
            text = font.render("It's a tie!", True, self.BLACK)

        text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.update()
        
    def main(self):
        # Main game loop that handles user inputs and game logic.
        self.draw_board()

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.player == 1:
                        x, y = pygame.mouse.get_pos()
                        col = x // self.SQUARE_SIZE
                        row = y // self.SQUARE_SIZE
                        if self.is_valid_move(row, col, self.player):
                            self.make_move(row, col, self.player)
                            self.player *= -1
                            self.draw_board()

                    if self.player == -1:
                        depth = 3
                        best_move = self.get_best_move(depth, self.player)
                        if best_move is not None:
                            row, col = best_move
                            self.make_move(row, col, self.player)
                            self.player *= -1
                            self.draw_board()

            valid_moves = self.get_valid_moves(self.player)
            if len(valid_moves) == 0:
                self.game_over = True
                score = self.evaluate_board()
                if score > 0:
                    print("White wins!")
                elif score < 0:
                    print("Blue wins!")
                else:
                    print("It's a tie!")
                break

if __name__ == "__main__":
    game = ReversiGame()
    game.main()