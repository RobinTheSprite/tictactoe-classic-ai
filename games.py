from algorithms import *
from constants import *
from utilities import *

def playerVersusRandom(save):
    print("Tic Tac Toe")
    print("Players: 1")

    board = 0
    boards = []
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

        boards.append(str(board) + "\n")

        board = randomMove(board, O)

        boards.append(str(board) + "\n")

        win = checkForWin(board)

    if save:
        writeGame(boards)

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
        boards.append(str(board) + "\n")

        board = randomMove(board, currentTurn)

        print()
        printBoard(board)
        print("Score: " + str(evaluate(board)))
        print()

        win = checkForWin(board)
        currentTurn, nextTurn = nextTurn, currentTurn

    if save:
        writeGame(boards)

    print()
    print("**************")
    print(win + " wins!")
    print("**************")


def playerVersusMinimax(save):
    print("Tic Tac Toe")
    print("Players: 1")

    board = 0
    boards = []
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

        boards.append(str(board) + "\n")

        board, valid = move(board, bestMove[0], bestMove[1], O)

        boards.append(str(board) + "\n")

        win = checkForWin(board)

    if save:
        writeGame(boards)

    print()
    printBoard(board)
    print()

    print("**************")
    print(win + " wins!")
    print("**************")


def minimaxVersusMinimax(save):
    print("Tic Tac Toe")
    print("Minimax")
    print("Players: 0")

    board = 0
    boards = []
    win = U
    currentTurn = (X, True)
    nextTurn = (O, False)
    boards.append(str(board) + "\n")
    while(win == U):
        bestScore, bestMove, searches = minimax(board, 0, 5, findEmptySpaces(board), currentTurn[1])
        board, valid = move(board, bestMove[0], bestMove[1], currentTurn[0])

        boards.append(str(board) + "\n")

        print()
        printBoard(board)
        print("Boards Searched: {}".format(searches))
        print()

        win = checkForWin(board)
        currentTurn, nextTurn = nextTurn, currentTurn

    if save:
        writeGame(boards)

    print()
    print("**************")
    print(win + " wins!")
    print("**************")


def alphaBetaVersusAlphaBeta(save):
    print("Tic Tac Toe")
    print("Alpha-Beta Search")
    print("Players: 0")

    board = 0
    boards = []
    win = U
    currentTurn = (X, True)
    nextTurn = (O, False)
    boards.append(str(board) + "\n")
    while(win == U):
        bestScore, bestMove, searches = alphaBeta(board, 0, 5, findEmptySpaces(board), currentTurn[1], -INF, INF)
        board, valid = move(board, bestMove[0], bestMove[1], currentTurn[0])

        boards.append(str(board) + "\n")

        print()
        printBoard(board)
        print("Boards Searched: {}".format(searches))
        print()

        win = checkForWin(board)
        currentTurn, nextTurn = nextTurn, currentTurn

    if save:
        writeGame(boards)

    print()
    print("**************")
    print(win + " wins!")
    print("**************")
