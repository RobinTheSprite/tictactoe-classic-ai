# tictactoe-classic-ai
### A demonstration of classic search algorithms in a game of 5x5 Tic-Tac-Toe

![Animation of alpha-beta search](tictactoe.GIF)

## Project structure
**games.py** contains several options for the algorithm to use for the AI:
1. Random moves
2. Minimax search
3. Alpha-Beta pruning
4. Monte Carlo Tree Search

To use one, call the computerVsComputer function at the bottom of games.py with the appropriate parameters. An example of MCTS and Alpha-Beta is the default.

**algorithms.py** contains the implementation of each algorithm.

**utilities.py** contains any functions necessary to play the game, such as making a move, printing the board, or selecting a node (for MCTS).

**constants.py** contains a number of constant global values used throughout the project, like the size of the board and the value of an "X" or an "O."

## Rules

The board is five rows by five columns.

Players take turns placing their symbol on the board.

X goes first.

Any horizontal, vertical, or diagonal row of four symbols wins the game.
