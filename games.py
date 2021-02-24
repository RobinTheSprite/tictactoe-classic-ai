from algorithms import *
from constants import *
from utilities import *

# To choose a game mode, pick a function and call it.
# Pass True to save the game, false otherwise.

def playerVersusRandom(save):
    print("Tic Tac Toe")
    print("Players: 1")

    board = 0
    boards = []
    win = UNFINISHED
    while(win == UNFINISHED):
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


def playerVersusMinimax(save):
    print("Tic Tac Toe")
    print("Players: 1")

    board = 0
    boards = []
    win = UNFINISHED
    while(win == UNFINISHED):
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

        _, bestMove, _ = minimax(board, 0, 2, findEmptySpaces(board), False)

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


def minimaxWrapper(board, currentTurn):
    _, bestMove, searches = minimax(board, 0, 3, findEmptySpaces(board), currentTurn)
    return bestMove, "Boards Searched: {}".format(searches)


def alphaBetaWrapper(board, currentTurn):
    _, bestMove, searches = alphaBeta(board, 0, 3, findEmptySpaces(board), currentTurn, -INF, INF)
    print(bestMove)
    return bestMove, "Boards Searched: {}".format(searches)


selectAlgorithm = {
    GameType.RANDOM: lambda board, currentTurn: random(board, currentTurn),
    GameType.MINIMAX: lambda board, currentTurn: minimaxWrapper(board, currentTurn),
    GameType.ALPHABETA: lambda board, currentTurn: alphaBetaWrapper(board, currentTurn),
    GameType.MONTECARLO: lambda board, currentTurn: monteCarlo(board, currentTurn, 15)
}

selectDescription = {
    GameType.RANDOM: "Random moves",
    GameType.MINIMAX: "Minimax",
    GameType.ALPHABETA: "Alpha-Beta Search",
    GameType.MONTECARLO: "Monte-Carlo Tree Search"
}

def computerVsComputer(gameType, save):
    print("Tic Tac Toe")
    print(selectDescription[gameType])
    print("Players: 0")

    board = 0
    boards = []
    win = UNFINISHED
    currentTurn = (X, True)
    nextTurn = (O, False)
    boards.append(str(board) + "\n")
    while(win == UNFINISHED):
        bestMove, statistic = selectAlgorithm[gameType](board, currentTurn[1])
        board, _ = move(board, bestMove[0], bestMove[1], currentTurn[0])

        boards.append(str(board) + "\n")

        print()
        printBoard(board)
        if statistic != str():
            print(statistic)
        print()

        win = checkForWin(board)
        currentTurn, nextTurn = nextTurn, currentTurn

    if save:
        writeGame(boards)

    print()
    print("**************")
    print(win + " wins!")
    print("**************")

computerVsComputer(GameType.MONTECARLO, False)