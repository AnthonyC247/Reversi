
# Reversi Game
This is a simple implementation of the Reversi (also known as Othello) game in Python. Reversi is a strategy board game for two players, played on an 8x8 grid. The goal of the game is to have the majority of your colored pieces on the board when the game ends.

## Data Structures
### `board`
The game board is represented as a 2D list with 8 rows and 8 columns. Each cell in the board can hold one of three values:
- 'X': Represents player 1's tile.
- 'O': Represents player 2's tile.
- ' ': Represents an empty cell.

### Data Structures Used
- **Lists**: Lists are used for various purposes such as representing the game board, storing valid moves, and iterating over coordinates.
- **Strings**: Strings are used to represent player tiles ('X' or 'O') and to create the horizontal and vertical lines for drawing the board.
- **Tuples**: Tuples are used for representing coordinate pairs (x, y) of potential moves.

## Functions
Here are the key functions used in this game:
- `drawBoard(board)`: Draws the game board on the console.
- `resetBoard(board)`: Resets the game board to the initial setup.
- `getNewBoard()`: Creates a new empty game board.
- `isValidMove(board, tile, xstart, ystart)`: Checks if a move is valid and returns the tiles that would be flipped.
- `isOnBoard(x, y)`: Checks if coordinates are within the game board.
- `getBoardWithValidMoves(board, tile)`: Returns a board with valid move locations marked with '.'.
- `getValidMoves(board, tile)`: Returns a list of valid move coordinates for a given player's tile.
- `getScoreOfBoard(board)`: Calculates the score of the game for each player.
- ... (and so on for other functions)

## Additional Features
The game provides the following additional features:
- Hints: You can toggle hints on/off to display valid move locations.
- Quit: You can quit the game at any time by typing 'quit'.
- Play Again: After the game ends, you can choose to play again or exit.

## Requirements
This game is written in Python and does not require any external libraries. Simply run the script using a Python interpreter.
