from constants import INF, X, O, UNFINISHED, X_WIN, O_WIN, NOBODY
from utilities import \
move, randomMove, boardDifference, \
checkForWin, evaluate, findEmptySpaces, \
makeEmptyNode, getChildren, uct, playout, select
from operator import itemgetter
from time import time
from random import randint


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


def monteCarlo(board, currentTurn, timeLimit):

    # Set up the root of the game tree
    root = makeEmptyNode()
    root["board"] = board
    root["isXsTurn"] = currentTurn
    root["unvisitedChildren"] = getChildren(root)

    # Set up some global statistics
    totalPlayouts = 0
    boardsSearched = 0
    startTime = time()
    while (time() - startTime) < timeLimit: # boardsSearched < 500000
        # Traverse the tree to find a node that's not fully explored
        currentNode = select(root)

        # Don't do a playout if this node ends the game
        winState = checkForWin(currentNode["board"])
        if winState == UNFINISHED:
            # Generate the child nodes if it hasn't been done yet
            if (len(currentNode["unvisitedChildren"]) == 0
            and len(currentNode["visitedChildren"]) == 0):
                currentNode["unvisitedChildren"] = getChildren(currentNode)

            # Choose a random unvisited child
            randomIndex = randint(0, len(currentNode["unvisitedChildren"]) - 1)
            child = currentNode["unvisitedChildren"][randomIndex]

            # Run a simulation from the child
            winState, b = playout(child)
            boardsSearched += b

            # Mark the child as visited and descend into it
            currentNode["unvisitedChildren"].pop(randomIndex)
            currentNode["visitedChildren"].append(child)
            currentNode = child

        totalPlayouts += 1

        while True:
            # Did we win?
            if ((winState == X and currentNode["isXsTurn"])
            or winState == O and not currentNode["isXsTurn"]):
                currentNode["wins"] += 1

            # Update playouts and UCT
            currentNode["playouts"] += 1
            currentNode["uct"] = uct(currentNode["wins"], currentNode["playouts"], 1.5, totalPlayouts)

            # Sort from highest UCT to lowest
            currentNode["visitedChildren"].sort(reverse=True, key=itemgetter("uct"))

            # Climb the tree
            if currentNode["parent"] == {}:
                root = currentNode
                break
            else:
                currentNode = currentNode["parent"]

    # Return the child with the most playouts
    bestChild = makeEmptyNode()
    for child in root["visitedChildren"]:
        if bestChild["playouts"] < child["playouts"]:
            bestChild = child
    return  boardDifference(root["board"], bestChild["board"]), \
            "Boards Searched: {}".format(boardsSearched)


