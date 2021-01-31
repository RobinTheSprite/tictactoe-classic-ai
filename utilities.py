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