from constants import *

def printBoard(board):
    mask = 0b11
    row = "|"
    for shift in range(30, -2, -2):
        space = ((mask << shift) & board) >> shift

        if space == EMPTY_BIN:
            row += " |"
        elif space == X_BIN:
            row += X + "|"
        elif space == O_BIN:
            row += O + "|"

        if shift % 8 == 0:
            print(row)
            row = "|"

def move(board, col, row, symbol):
    maxShift = 30
    mask = 0b11

    shift = maxShift - 2*col - 8*row

    if (board & (mask << shift)) != 0:
        return board, False

    binarySymbol = 0
    if symbol == X:
        binarySymbol = X_BIN
    elif symbol == O:
        binarySymbol = O_BIN

    board = board | (binarySymbol << shift)

    return board, True

def isWin(board, winState):
    mask = 0b11
    accumulator = 0
    board = board & winState
    total = 0

    while board != 0:
        space = (board & mask)
        accumulator = accumulator | space
        total += space
        board = board >> 2

    if accumulator == X_BIN and total == X_WIN:
        return X
    elif accumulator == O_BIN and total == O_WIN:
        return O
    else:
        return N


def checkForWin(board):
    result = str()
    for winState in WIN_STATES:
        result = isWin(board, winState)
        if result != N:
            return result

    return N