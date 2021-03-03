from constants import INF, X, O, UNFINISHED, X_WIN, O_WIN, NOBODY
from utilities import \
move, randomMove, boardDifference, \
checkForWin, evaluate, findEmptySpaces, \
makeEmptyNode, getChildren, uct, playout
from operator import itemgetter
from time import time


def random(board, currentTurn):
    return boardDifference(board, randomMove(board, X if currentTurn else O)), str()


def minimax(board, currentDepth, maxDepth, emptySpaces, isXsTurn):
    evaluation = evaluate(board)
    if currentDepth == maxDepth or abs(evaluation) == abs(X_WIN):
        return evaluation, (), 0

    optimalMove = ()
    searches = 0
    if isXsTurn:
        optimalScore = -INF
        for space in emptySpaces:
            nextState, _ = move(board, space[0], space[1], X)

            nextScore, _, subtreeSearches = minimax(
                nextState,
                currentDepth + 1,
                maxDepth,
                findEmptySpaces(nextState),
                False
            )

            searches += 1 + subtreeSearches

            if optimalScore < nextScore:
                optimalScore = nextScore
                optimalMove = space
    else:
        optimalScore = INF
        for space in emptySpaces:
            nextState, _ = move(board, space[0], space[1], O)

            nextScore, _, subtreeSearches = minimax(
                nextState,
                currentDepth + 1,
                maxDepth,
                findEmptySpaces(nextState),
                True
            )

            searches += 1 + subtreeSearches

            if optimalScore > nextScore:
                optimalScore = nextScore
                optimalMove = space

    """ Debug string:
        print(
            "Depth: {}, Empty Spaces: {}, X's turn: {}, Score: {}, Move: {}, Searches: {}"
            .format(currentDepth, len(emptySpaces), isXsTurn, optimalScore, optimalMove, searches)
        )
    """

    return optimalScore, optimalMove, searches


def alphaBeta(board, currentDepth, maxDepth, emptySpaces, isXsTurn, alpha, beta):
    evaluation = evaluate(board)
    if currentDepth == maxDepth or abs(evaluation) == abs(X_WIN):
        return evaluation, (), 0

    optimalMove = ()
    searches = 0
    if isXsTurn:
        optimalScore = -INF
        for space in emptySpaces:
            nextState, _ = move(board, space[0], space[1], X)

            nextScore, _, subtreeSearches = alphaBeta(
                nextState,
                currentDepth + 1,
                maxDepth,
                findEmptySpaces(nextState),
                False,
                alpha,
                beta
            )

            searches += 1 + subtreeSearches

            if optimalScore < nextScore:
                optimalScore = nextScore
                optimalMove = space

                alpha = max(alpha, optimalScore)
            if beta <= alpha:
                break
    else:
        optimalScore = INF
        for space in emptySpaces:
            nextState, _ = move(board, space[0], space[1], O)

            nextScore, _, subtreeSearches = alphaBeta(
                nextState,
                currentDepth + 1,
                maxDepth,
                findEmptySpaces(nextState),
                True,
                alpha,
                beta
            )

            searches += 1 + subtreeSearches

            if optimalScore > nextScore:
                optimalScore = nextScore
                optimalMove = space

                beta = min(beta, optimalScore)
            if beta <= alpha:
                break

    return optimalScore, optimalMove, searches

# A leaf node is one with an empty list []
def monteCarlo(board, currentTurn, timeLimit):
    root = makeEmptyNode()
    root["board"] = board
    root["isXsTurn"] = currentTurn
    root["unvisitedChildren"] = getChildren(root)

    totalPlayouts = 0

    boardsSearched = 0
    startTime = time()
    while (time() - startTime) < timeLimit:
        currentNode = root

        while (len(currentNode["unvisitedChildren"]) == 0
            and len(currentNode["visitedChildren"]) > 0):
            currentNode = currentNode["visitedChildren"][0]

        winState = checkForWin(currentNode["board"])
        if winState == X or winState == O or winState == NOBODY:
            currentNode["playouts"] += 1
            totalPlayouts += 1

            if winState == NOBODY:
                currentNode["ties"] += 1
        else:
            if (len(currentNode["unvisitedChildren"]) == 0
            and len(currentNode["visitedChildren"]) == 0):
                currentNode["unvisitedChildren"] = getChildren(currentNode)

            child = currentNode["unvisitedChildren"][0]

            winState, b = playout(child)
            boardsSearched += b

            if winState == NOBODY:
                child["ties"] += 1

            child["playouts"] += 1
            totalPlayouts += 1
            currentNode["unvisitedChildren"].pop(0)
            currentNode["visitedChildren"].append(child)

        while True:
            playoutsForCurrent = 0
            lossesForCurrent = 0
            tiesForCurrent = 0
            for child in currentNode["visitedChildren"]:
                child["uct"] = uct(child["wins"], child["playouts"], 1.5, totalPlayouts)
                playoutsForCurrent += child["playouts"]
                lossesForCurrent += child["wins"]
                tiesForCurrent += child["ties"]

            currentNode["visitedChildren"].sort(reverse=True, key=itemgetter("uct"))
            currentNode["playouts"] = max(playoutsForCurrent, currentNode["playouts"])
            currentNode["ties"] = tiesForCurrent
            currentNode["wins"] = playoutsForCurrent - lossesForCurrent - tiesForCurrent

            if currentNode["parent"] == {}:
                root = currentNode
                break
            else:
                currentNode = currentNode["parent"]

    bestChild = makeEmptyNode()
    for child in root["visitedChildren"]:
        if bestChild["playouts"] < child["playouts"]:
            bestChild = child
    return  boardDifference(root["board"], bestChild["board"]), \
            "Boards Searched: {}".format(boardsSearched)


