from tictactoe import *
from constants import *

def playerVersusRandom():
    print("Tic Tac Toe")
    print("Players: 1")

    board = 0
    win = N
    while(win == N):
        valid = False
        while not valid:
            print()
            printBoard(board)
            print()
            print("Column:")
            col = input()
            print("Row:")
            row = input()

            if len(col) == 0 or len(row) == 0:
                break

            board, valid = move(board, int(col) - 1, int(row) - 1, X)
            if not valid:
                print("That space is taken")

        board = randomMove(board, O)

        win = checkForWin(board)

    print()
    printBoard(board)
    print()

    print("**************")
    print(win + " wins!")
    print("**************")


def randomVersusRandom():
    print("Tic Tac Toe")
    print("Players: 0")

    board = 0
    win = N
    currentTurn = X
    nextTurn = O
    while(win == N):
        board = randomMove(board, currentTurn)

        print()
        printBoard(board)
        print("Score: " + str(evaluate(board)))
        print()

        win = checkForWin(board)
        currentTurn, nextTurn = nextTurn, currentTurn

    print()
    print("**************")
    print(win + " wins!")
    print("**************")


def playerVersusMinimax():
    print("Tic Tac Toe")
    print("Players: 1")

    board = 0
    win = N
    while(win == N):
        valid = False
        while not valid:
            print()
            printBoard(board)
            print()
            print("Column:")
            col = input()
            print("Row:")
            row = input()

            if len(col) == 0 or len(row) == 0:
                break

            board, valid = move(board, int(col) - 1, int(row) - 1, X)
            if not valid:
                print("That space is taken")

        bestScore, bestMove = minimax(board, 0, 2, findEmptySpaces(board), False)

        board, valid = move(board, bestMove[0], bestMove[1], O)

        win = checkForWin(board)

    print()
    printBoard(board)
    print()

    print("**************")
    print(win + " wins!")
    print("**************")

playerVersusMinimax()