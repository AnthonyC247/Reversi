'''Hello! This will be my walkthrough of how to create the Reversi/Othello game 
    originally invented by Goro Hasegawa'''
#Set up the necessary modules
import pygame 
import sys
import numpy as np

#Initialize the game
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size) #To correspond with the appropriate display of the game
pygame.display.set_caption("Reversi")

#Set up the colors of the screen
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 128, 0)
red = (255, 0, 0)

#Board and game constraints
rows, cols = 8
square_size = width // cols

#create the initial game board 
board = np.zeros((rows, cols), dtype=int)

#Now to create the game board on the screen
screen.fill(green)
for row in range(rows):
    for col in range(cols):
        pygame.draw.rect(screen, black, (col * square_size, row * square_size, square_size, square_size))
        if board[row][col] == 1:
            pygame.draw.rect(screen, white, (col * square_size + square_size // 2, row * square_size + square_size // 2), square_size // 2 - 5)
        elif board[row][col] == -1:
            pygame.draw.circle(screen, red, (col * square_size + square_size // 2, row * square_size + square_size // 2), square_size // 2 - 5)
pygame.display.update()