import pygame
import sys
import numpy as np

# Initialize the game
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Reversi/Othello")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)

# An 8 by 8 board as a 2 dimensional Numpy arrary
ROWS = COLS = 8
SQUARE_SIZE = width // COLS

# Create the initial game board
board = np.zeros((ROWS, COLS))


def draw_board():
    # Draw the game board on the screen
    # Iterating over each square to draw each individual cell to be filled with color
    screen.fill(GREEN)
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if board[row][col] == 1: #Checking the value of the board at current position 
                pygame.draw.circle(screen, WHITE, (
                    col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            elif board[row][col] == -1:
                pygame.draw.circle(screen, BLUE, (
                    col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
    pygame.display.update()

# A function returning the list of valid moves for the given player
# Checking if move is valid for the current player
def get_valid_moves(board, player):
    valid_moves = []
    for row in range(ROWS):
        for col in range(COLS):
            if is_valid_move(board, row, col, player):
                valid_moves.append((row, col))
    return valid_moves

# A function checking if a move is valid for the current player at current location of row and column 
# Will iterate over all possible directions of left, right, up, down and diagonally
# The is_valid_move function is called to verify if move performed adheres to any of the possible directions
def is_valid_move(board, row, col, player):
    if board[row][col] != 0:
        return False
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
    for direction in directions:
        if is_valid_direction(board, row, col, player, direction):
            return True
    return False

# A function checking if the move made by the player is valid 
# Will in given directions made by the player until value of the direction reaches the end 
def is_valid_direction(board, row, col, player, direction):
    delta_row, delta_col = direction
    current_row, current_col = row + delta_row, col + delta_col
    if not (0 <= current_row < ROWS and 0 <= current_col < COLS and board[current_row][current_col] == -player):
        return False
    flips = []
    while 0 <= current_row < ROWS and 0 <= current_col < COLS:
        if board[current_row][current_col] == 0:
            return False
        elif board[current_row][current_col] == player:
            for flip in flips:
                flip_row, flip_col = flip
                board[flip_row][flip_col] = player
            return True
        flips.append((current_row, current_col))
        current_row += delta_row
        current_col += delta_col
    return False

# A function that makes a move for the current player 
def make_move(board, row, col, player):
    board[row][col] = player
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
    for direction in directions:
        if is_valid_direction(board, row, col, player, direction):
            flip_pieces(board, row, col, player, direction)

# A function flipping the opponents pieces in the specified starting direction
def flip_pieces(board, row, col, player, direction):
    delta_row, delta_col = direction
    current_row, current_col = row + delta_row, col + delta_col
    while board[current_row][current_col] == -player:
        board[current_row][current_col] = player
        current_row += delta_row
        current_col += delta_col

# A function evaluating the current state (score) of the board
def evaluate_board(board):
    score = np.sum(board)
    return score

# The function containing the logic of the game
def minimax(board, depth, maximizing_player):
    if depth == 0:
        return evaluate_board(board) # Return evaluation score of the board
    
    valid_moves = get_valid_moves(board, 1 if maximizing_player else -1) # Generate valid moves for current player
    if maximizing_player:
        max_eval = float('-inf')
        for move in valid_moves:
            row, col = move
            new_board = board.copy()
            make_move(new_board, row, col, 1)
            eval = minimax(new_board, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in valid_moves:
            row, col = move
            new_board = board.copy()
            make_move(new_board, row, col, -1)
            eval = minimax(new_board, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval

# Finding the best move for the current player using the minimax algorithm
def get_best_move(board, depth, player):
    valid_moves = get_valid_moves(board, player)
    best_eval = float('-inf')
    best_move = None
    for move in valid_moves:
        row, col = move
        new_board = board.copy()
        make_move(new_board, row, col, player)
        eval = minimax(new_board, depth - 1, False)
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move


# Main game loop
def main():
    player = 1
    game_over = False # Boolean expression that game is not over when starting 
    draw_board()
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player == 1:
                    # Human player's turn
                    x, y = pygame.mouse.get_pos()
                    col = x // SQUARE_SIZE
                    row = y // SQUARE_SIZE
                    if is_valid_move(board, row, col, player):
                        make_move(board, row, col, player)
                        player *= -1
                        draw_board()

                if player == -1:
                    # AI player's turn
                    depth = 3
                    best_move = get_best_move(board, depth, player)
                    if best_move is not None:
                        row, col = best_move
                        make_move(board, row, col, player)
                        player *= -1
                        draw_board()

        valid_moves = get_valid_moves(board, player)
        if len(valid_moves) == 0:
            game_over = True
            score = evaluate_board(board)
            if score > 0:
                print("White wins!")
            elif score < 0:
                print("Blue wins!")
            else:
                print("It's a tie!")
            break


if __name__ == "__main__":
    main()
