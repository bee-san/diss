"""
Class to make the maze in Python
"""

import numpy as np
import operator

class maze:
    def __init__(self):
        self.maze = np.array([
            [ 1,  0,  1,  1,  1,  1,  1,  1,  1,  1],
            [ 1,  1,  1,  1,  1,  0,  1,  1,  1,  1],
            [ 1,  1,  1,  1,  1,  0,  1,  1,  1,  1],
            [ 0,  0,  1,  0,  0,  1,  0,  1,  1,  1],
            [ 1,  1,  0,  1,  0,  1,  0,  0,  0,  1],
            [ 1,  1,  0,  1,  0,  1,  1,  1,  1,  1],
            [ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1],
            [ 1,  1,  1,  1,  1,  1,  0,  0,  0,  0],
            [ 1,  0,  0,  0,  0,  0,  1,  1,  1,  1],
            [ 1,  1,  1,  1,  1,  1,  1,  0,  1,  1]
        ])
        self.row = 10
        self.col = 10

    def getMaze():
        return self.maze
    def getSizeOfMaze():
        return len(self.maze)
    def vectorAddition(self, tup1, tup2):
        # since we want to add coords together element wise
        # (0, 0) + (1, 1) = (0, 0, 1, 1). this makes the result (1, 1).
        # https://stackoverflow.com/questions/497885/python-element-wise-tuple-operations-like-sum
        return tuple(map(operator.add, tup1, tup2))


    def getLegalMoves(self, coords):
        # 0 is a wall
        # 1 is valid
        moves = {"Up": (1, 0), "Down": (-1, 0), "Left": (0, -1), "Right": (0, 1)}
        legalMoves = {}
        for move in moves:
            try:
                print(self.vectorAddition(coords, moves[move]))
                newCoords = self.vectorAddition(coords, moves[move])
                # checks to see if there is an illegal move
                negativeCoords = True if any(y < 0 for y in x) else False
                outsideMap = True if any(y > len(self.maze[0]) - 1 for y in newCoords) else False
                illegalMove = True if negativeCoords + outsideMap == True else False
                if not illegalMove and newCoords != 0:
                    legalMoves[move] = moves[move]
                    # append to dictionary
                    
            except IndexError as e:
                print("Index error")
                # Not a valid move as it goes out of bounds
                continue
        return legalMoves

m = maze()
coords = (5, 5)
print(coords)
print(m.getLegalMoves(coords))
# dist = np.sqrt(((a[:, None] - b[:, :, None]) ** 2).sum(0))