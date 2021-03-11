from algorithms import random, minimax, alphaBeta, monteCarlo
from constants import X, O, UNFINISHED, GameType, INF
from utilities import \
printBoard, randomMove, move, \
checkForWin, writeGame, findEmptySpaces
from time import time

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

            board, valid = move(board, int(col), int(row), X)
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

            board, valid = move(board, int(col), int(row), X)
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

def computerVsComputer(gameTypes, save):
    print("Tic Tac Toe")
    print("{} versus {}".format(
        selectDescription[gameTypes[0]],
        selectDescription[gameTypes[1]]
    ))
    print("Players: 0")

    board = 0
    boards = []
    win = UNFINISHED
    currentTurn = (X, True, gameTypes[0])
    nextTurn = (O, False, gameTypes[1])
    boards.append(str(board) + "\n")
    while(win == UNFINISHED):
        startTime = time()
        bestMove, statistic = selectAlgorithm[currentTurn[2]](board, currentTurn[1])
        duration = time() - startTime
        board, _ = move(board, bestMove[0], bestMove[1], currentTurn[0])

        boards.append(str(board) + "\n")

        print()
        printBoard(board)
        if statistic != str():
            print(statistic)
        print("Time: {} seconds".format(round(duration, 4)))
        print()

        win = checkForWin(board)
        currentTurn, nextTurn = nextTurn, currentTurn

    if save:
        writeGame(boards)

    print()
    print("**************")
    print(win + " wins!")
    print("**************")

computerVsComputer((GameType.MONTECARLO, GameType.ALPHABETA), False)