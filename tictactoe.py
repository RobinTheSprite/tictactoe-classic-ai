from constants import *
from utilities import *


def minimax(board, currentDepth, maxDepth, emptySpaces, isXsTurn):
    evaluation = evaluate(board)
    if currentDepth == maxDepth or abs(evaluation) == abs(X_WIN):
        return evaluation, (), 0

    optimalMove = ()
    searches = 0
    if isXsTurn:
        optimalScore = O_WIN
        for space in emptySpaces:
            nextState, valid = move(board, space[0], space[1], X)

            nextScore, nextMove, subtreeSearches = minimax(
                nextState,
                currentDepth + 1,
                maxDepth,
                findEmptySpaces(nextState),
                False
            )

            searches += 1 + subtreeSearches

            if optimalScore <= nextScore:
                optimalScore = nextScore
                optimalMove = space
    else:
        optimalScore = X_WIN
        for space in emptySpaces:
            nextState, valid = move(board, space[0], space[1], O)

            nextScore, nextMove, subtreeSearches = minimax(
                nextState,
                currentDepth + 1,
                maxDepth,
                findEmptySpaces(nextState),
                True
            )

            searches += 1 + subtreeSearches

            if optimalScore >= nextScore:
                optimalScore = nextScore
                optimalMove = space

    return optimalScore, optimalMove, searches
