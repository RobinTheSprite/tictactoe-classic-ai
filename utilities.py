from constants import *
from random import choice
from time import time, sleep
from keyboard import is_pressed
from math import sqrt, log

def printBoard(board):
    mask = 0b11
    row = "|"

    # For all the spaces on the board:
    for shift in range(MAX_SHIFT, -2, -2):
        space = ((mask << shift) & board) >> shift

        # Print the appropriate symbol for each space
        if space == EMPTY_BIN:
            row += " |"
        elif space == X_BIN:
            row += X + "|"
        elif space == O_BIN:
            row += O + "|"

        # Print the side of the board at the beginning of a row
        if shift % (BOARD_LENGTH*2) == 0:
            print(row)
            row = "|"


def boardDifference(board1, board2):
    difference = board1 ^ board2

    mask = 0b11
    for row in range(0, BOARD_LENGTH):
        for col in range(0, BOARD_LENGTH):
            shift = MAX_SHIFT - 2*col - BOARD_LENGTH*2*row
            space = (mask << shift) & difference

            if space != EMPTY_BIN:
                return (col, row)


def getUsedSpaces(board):
    return (board & USED_SPACES_MASK) >> MAX_SHIFT + 2


def setUsedSpaces(board, usedSpaces):
    return board & (~USED_SPACES_MASK) | (usedSpaces << MAX_SHIFT + 2)


def move(board, col, row, symbol):
    mask = 0b11

    shift = MAX_SHIFT - 2*col - BOARD_LENGTH*2*row

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

    # Increment the count of used spaces
    usedSpaces = getUsedSpaces(board)
    usedSpaces += 1
    board = setUsedSpaces(board, usedSpaces)

    return board, True


def checkForWin(board):
    for winState in WIN_STATES:
        maskedBoard = board & winState
        if maskedBoard == winState & X_MASK:
            return X
        elif maskedBoard == winState & O_MASK:
            return O

    if getUsedSpaces(board) == NUM_OF_SPACES:
        return NOBODY
    else:
        return UNFINISHED


def findEmptySpaces(board):
    emptySpaces = []
    mask = 0b11

    if getUsedSpaces(board) != NUM_OF_SPACES:
        # For each space on the board:
        for col in range(BOARD_LENGTH):
            for row in range(BOARD_LENGTH):
                shift = MAX_SHIFT - 2*col - BOARD_LENGTH*2*row

                # Append tuple(col, row) if the space is empty
                if (board & (mask << shift)) == EMPTY_BIN:
                    emptySpaces.append((col, row))

    return emptySpaces


def randomMove(board, symbol):
    spaces = findEmptySpaces(board)

    lenSpaces = len(spaces)
    # Choose a random space
    if lenSpaces != 0:
        randomSpace = choice(spaces)
        board, _ = move(board, randomSpace[0], randomSpace[1], symbol)

    return board


def evaluate(board):
    mask = 0b11
    total = 0

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

            total -= 1
        elif numberOfOs == 0 and numberOfXs > 0:
            if numberOfXs == 4:
                return X_WIN

            total += 1

    return total



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
        )[0]
        child["isXsTurn"] = not currentNode["isXsTurn"]
        child["parent"] = currentNode

        children.append(child)

    return children


def playout(child):
    boardsSearched = 0
    childBoard = child["board"]
    winState = checkForWin(childBoard)
    currentTurn = X if child["isXsTurn"] else O
    nextTurn = X if not child["isXsTurn"] else O

    while winState == UNFINISHED:
        boardsSearched += 1
        childBoard = randomMove(childBoard, currentTurn)
        currentTurn, nextTurn = nextTurn, currentTurn
        winState = checkForWin(childBoard)

    return winState, boardsSearched


def uct(w, n, c, N):
    return w / n + c * sqrt(log(N) / n)


def select(currentNode):
    bestChild = currentNode
    bestUCT = -1
    searchStack = [currentNode]

    # currentNode is always the root to begin with,
    # so don't search unless the root is fully expanded
    if len(currentNode["unvisitedChildren"]) == 0:
        while len(searchStack):
            currentNode = searchStack.pop()
            if len(currentNode["unvisitedChildren"]):
                nodeUCT = uct(currentNode["wins"], currentNode["playouts"], 1.5, currentNode["parent"]["playouts"])

                if nodeUCT > bestUCT:
                    bestUCT = nodeUCT
                    bestChild = currentNode

            for child in currentNode["visitedChildren"]:
                searchStack.append(child)

    return bestChild