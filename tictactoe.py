from constants import *
from utilities import *


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
