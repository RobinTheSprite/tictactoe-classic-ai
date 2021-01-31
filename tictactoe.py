from constants import *
from utilities import *

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
        return evaluate(board), ()

    optimalMove = ()
    if isXsTurn:
        optimalScore = O_WIN
        for space in emptySpaces:
            nextState, valid = move(board, space[0], space[1], X)

            nextScore, nextMove = minimax(
                nextState,
                currentDepth + 1,
                maxDepth,
                findEmptySpaces(nextState),
                False
            )

            if optimalScore <= nextScore:
                optimalScore = nextScore
                optimalMove = space
                if optimalScore == X_WIN:
                    break
    else:
        optimalScore = X_WIN
        for space in emptySpaces:
            nextState, valid = move(board, space[0], space[1], O)

            nextScore, nextMove = minimax(
                nextState,
                currentDepth + 1,
                maxDepth,
                findEmptySpaces(nextState),
                True
            )

            if optimalScore >= nextScore:
                optimalScore = nextScore
                optimalMove = space
                if optimalScore == O_WIN:
                    break

    return optimalScore, optimalMove
