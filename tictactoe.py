from constants import *
from random import sample

def printBoard(board):
    mask = 0b11
    row = "|"
    maxShift = BOARD_SIZE**2 * 2 - 2

    for shift in range(maxShift, -2, -2):
        space = ((mask << shift) & board) >> shift

        if space == EMPTY_BIN:
            row += " |"
        elif space == X_BIN:
            row += X + "|"
        elif space == O_BIN:
            row += O + "|"

        if shift % (BOARD_SIZE*2) == 0:
            print(row)
            row = "|"

def move(board, col, row, symbol):
    maxShift = BOARD_SIZE**2 * 2 - 2
    mask = 0b11

    shift = maxShift - 2*col - BOARD_SIZE*2*row

    if (board & (mask << shift)) != 0:
        return board, False

    binarySymbol = 0
    if symbol == X:
        binarySymbol = X_BIN
    elif symbol == O:
        binarySymbol = O_BIN

    board = board | (binarySymbol << shift)

    return board, True


def checkForWin(board):
    score = evaluate(board)
    if score == X_WIN:
        return X
    elif score == O_WIN:
        return O
    elif score == N_WIN:
        return N
    else:
        return U


def findEmptySpaces(board):
    emptySpaces = []
    maxShift = BOARD_SIZE**2 * 2 - 2
    mask = 0b11

    for col in range(5):
        for row in range(5):
            shift = maxShift - 2*col - BOARD_SIZE*2*row

            if (board & (mask << shift)) == EMPTY_BIN:
                emptySpaces.append((col, row))

    return emptySpaces


def randomMove(board, symbol):
    valid = False
    while not valid:
        spaces = findEmptySpaces(board)

        space = sample(spaces, 1)[0]

        board, valid = move(board, space[0], space[1], symbol)

    return board


def evaluate(board):
    mask = 0b11
    total = 0
    winFound = False

    for winState in WIN_STATES:
        maskedBoard = board & winState

        numberOfXs = 0
        numberOfOs = 0
        while maskedBoard != 0:
            space = (maskedBoard & mask)
            if space == X_BIN:
                numberOfXs += 1
            elif space == O_BIN:
                numberOfOs += 1
            maskedBoard = maskedBoard >> 2

        if numberOfXs == 0 and numberOfOs > 0:
            if numberOfOs == 4:
                return O_WIN

            winFound = True
            total -= 1
        elif numberOfOs == 0 and numberOfXs > 0:
            if numberOfXs == 4:
                return X_WIN

            winFound = True
            total += 1

    if winFound:
    return total
    else:
        return N_WIN


def minimax(board, currentDepth, maxDepth, emptySpaces, isXsTurn):
    if currentDepth == maxDepth:
        printBoard(board)
        print()
        return evaluate(board), board

    optimalScore = 0
    optimalMove = ()
    if isXsTurn:
        for space in emptySpaces:
            nextState, valid = move(board, space[0], space[1], X)

            nextScore, nextMove = minimax(
                nextState,
                currentDepth + 1,
                maxDepth,
                findEmptySpaces(nextState),
                False
            )

            if optimalScore < nextScore:
                optimalScore = nextScore
                optimalMove = nextState
                if optimalScore == X_WIN:
                    break
    else:
        for space in emptySpaces:
            nextState, valid = move(board, space[0], space[1], O)

            nextScore, nextMove = minimax(
                nextState,
                currentDepth + 1,
                maxDepth,
                findEmptySpaces(nextState),
                True
            )

            if optimalScore > nextScore:
                optimalScore = nextScore
                optimalMove = nextState
                if optimalScore == O_WIN:
                    break

    return optimalScore, optimalMove
