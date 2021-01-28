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

    if accumulator == X_BIN and total == X_WIN_TOTAL:
        return X
    elif accumulator == O_BIN and total == O_WIN_TOTAL:
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
    maxX = 0
    maxO = 0

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
            maxO = max(maxO, numberOfOs)
        elif numberOfOs == 0 and numberOfXs > 0:
            maxX = max(maxX, numberOfXs)

    if maxO > maxX:
        return -maxO
    elif maxO < maxX:
        return maxX
    else:
        return 0


def playerVersusComputer():
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


def computerVersusComputer():
    print("Tic Tac Toe")
    print("Players: 0")

    board = 0
    win = N
    while(win == N):
        board = randomMove(board, X)

        print()
        printBoard(board)
        print()

        board = randomMove(board, O)
        printBoard(board)

        win = checkForWin(board)

    print()
    print("**************")
    print(win + " wins!")
    print("**************")