from constants import *
from random import sample
from time import time, sleep
from keyboard import is_pressed
from math import sqrt, log

def printBoard(board):
    mask = 0b11
    row = "|"
    maxShift = BOARD_SIZE**2 * 2 - 2

    # For all the spaces on the board:
    for shift in range(maxShift, -2, -2):
        space = ((mask << shift) & board) >> shift

        # Print the appropriate symbol for each space
        if space == EMPTY_BIN:
            row += " |"
        elif space == X_BIN:
            row += X + "|"
        elif space == O_BIN:
            row += O + "|"

        # Print the side of the board at the beginning of a row
        if shift % (BOARD_SIZE*2) == 0:
            print(row)
            row = "|"

def move(board, col, row, symbol):
    maxShift = BOARD_SIZE**2 * 2 - 2
    mask = 0b11

    shift = maxShift - 2*col - BOARD_SIZE*2*row

    # If that space is occupied already:
    if (board & (mask << shift)) != 0:
        return board, False

    # Choose a symbol to print
    binarySymbol = 0
    if symbol == X:
        binarySymbol = X_BIN
    elif symbol == O:
        binarySymbol = O_BIN

    # Place the symbol on the board
    board = board | (binarySymbol << shift)

    return board, True


def checkForWin(board):
    score = evaluate(board)
    if score == X_WIN:
        return X
    elif score == O_WIN:
        return O
    elif score == NO_WIN:
        return NOBODY # Tied game
    else:
        return UNFINISHED # Game's not over


def findEmptySpaces(board):
    emptySpaces = []
    maxShift = BOARD_SIZE**2 * 2 - 2
    mask = 0b11

    # For each space on the board:
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE):
            shift = maxShift - 2*col - BOARD_SIZE*2*row

            # Append tuple(col, row) if the space is empty
            if (board & (mask << shift)) == EMPTY_BIN:
                emptySpaces.append((col, row))

    return emptySpaces


def randomMove(board, symbol):
    valid = False
    while not valid:
        spaces = findEmptySpaces(board)

        # Choose a random space
        randomSpace = sample(spaces, 1)[0]

        board, valid = move(board, randomSpace[0], randomSpace[1], symbol)

    return board


def evaluate(board):
    mask = 0b11
    total = 0
    winFound = False

    for winState in WIN_STATES:
        # Mask out everything except the symbols in the win state
        maskedBoard = board & winState

        # Count the number of Xs and Os in the win state
        numberOfXs = 0
        numberOfOs = 0
        while maskedBoard != 0:
            space = (maskedBoard & mask)
            if space == X_BIN:
                numberOfXs += 1
            elif space == O_BIN:
                numberOfOs += 1
            maskedBoard = maskedBoard >> 2

        # Figure out if X or O could use this win state to win.
        # If so, count it in the grand total
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

    # Tells the difference between a sum of 0 and a tie
    if winFound:
        return total
    else:
        return NO_WIN


def writeGame(boards):
    timestamp = time()
    f = open("games/game-{}.sav".format(timestamp), "w")
    f.writelines(boards)
    f.close()

def playbackGame(filename):
    print(filename)

    current = 0
    f = open(filename, "r")
    lines = f.readlines()
    while current < len(lines):
        print()
        printBoard(int(lines[current]))
        print("Press ENTER to quit")

        # Slow the user's input down
        sleep(0.1)

        # Right arrow to go back one turn,
        # Left arrow to go forward one turn,
        # ENTER to quit
        while True:
            if is_pressed("left") and current > 0:
                current -= 1
                break
            elif is_pressed("right") and current < len(lines) - 1:
                current += 1
                break
            elif is_pressed("enter"):
                current = len(lines)
                break

    #Get the last line as int to check for a win
    win = checkForWin(int(lines[len(lines) - 1]))

    print()
    print("**************")
    print(win + " wins!")
    print("**************")


def makeEmptyNode():
    return {
        "board": 0,
        "playouts": 0,
        "wins": 0,
        "ties": 0,
        "uct": 0,
        "isXsTurn": True,
        "visitedChildren": [],
        "unvisitedChildren": [],
        "parent": {}
    }


def getChildren(currentNode):
    children = []
    spaces = findEmptySpaces(currentNode["board"])
    for space in spaces:

        child = makeEmptyNode()

        child["board"] = move(
            currentNode["board"],
            space[0],
            space[1],
            X if currentNode["isXsTurn"] else O
        )
        child["isXsTurn"] = not currentNode["isXsTurn"]
        child["parent"] = currentNode

        children.append(child)

    return children

def uct(w, n, c, N):
    return (w/n) + c * sqrt(log(N) / n)