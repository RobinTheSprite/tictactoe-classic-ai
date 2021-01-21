from constants import *

def printBoard(board):
    mask = 0b11
    row = "|"
    for shift in range(30, -2, -2):
        space = ((mask << shift) & board) >> shift

        if space == 0:
            row += " |"
        elif space == 1:
            row += X + "|"
        elif space == 2:
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
        binarySymbol = 1
    elif symbol == O:
        binarySymbol = 2

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

    if accumulator == 1 and total == 3:
        return X
    elif accumulator == 2 and total == 6:
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