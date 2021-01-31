from tictactoe import *
from constants import *
from utilities import *

def playerVersusRandom():
    print("Tic Tac Toe")
    print("Players: 1")

    board = 0
    win = U
    while(win == U):
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


def randomVersusRandom(save):
    print("Tic Tac Toe")
    print("Players: 0")

    board = 0
    boards = []
    win = U
    currentTurn = X
    nextTurn = O
    while(win == U):
        board = randomMove(board, currentTurn)

        print()
        printBoard(board)
        print("Score: " + str(evaluate(board)))
        print()

        boards.append(str(board) + "\n")

        win = checkForWin(board)
        currentTurn, nextTurn = nextTurn, currentTurn

    if save:
        writeGame(boards)

    print()
    print("**************")
    print(win + " wins!")
    print("**************")


def playerVersusMinimax():
    print("Tic Tac Toe")
    print("Players: 1")

    board = 0
    win = U
    while(win == U):
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

        bestScore, bestMove, searches = minimax(board, 0, 2, findEmptySpaces(board), False)

        board, valid = move(board, bestMove[0], bestMove[1], O)

        win = checkForWin(board)

    print()
    printBoard(board)
    print()

    print("**************")
    print(win + " wins!")
    print("**************")


def minimaxVersusMinimax():
    print("Tic Tac Toe")
    print("Players: 0")

    board = 0
    win = U
    currentTurn = (X, True)
    nextTurn = (O, False)
    while(win == U):
        bestScore, bestMove, searches = minimax(board, 0, 3, findEmptySpaces(board), currentTurn[1])
        board, valid = move(board, bestMove[0], bestMove[1], currentTurn[0])

        print()
        printBoard(board)
        print("Boards Searched: {}".format(searches))
        print()

        win = checkForWin(board)
        currentTurn, nextTurn = nextTurn, currentTurn

    print()
    print("**************")
    print(win + " wins!")
    print("**************")


playbackGame("games/game-1612053474.7294028.sav")