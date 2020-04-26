"""
Class to make the maze in Python
"""

import numpy as np
import Qagent
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
        self.agentLocation = (0, 0)
        self.moves = {"Up": (1, 0), "Down": (-1, 0), "Left": (0, -1), "Right": (0, 1)}

    def getMaze(self):
        return self.maze
    def getSizeOfMaze(self):
        return len(self.maze)
    def vectorAddition(self, tup1, tup2):
        if tup1 == 0:
            tup1 = (0, 0)
        # since we want to add coords together element wise
        # (0, 0) + (1, 1) = (0, 0, 1, 1). this makes the result (1, 1).
        # https://stackoverflow.com/questions/497885/python-element-wise-tuple-operations-like-sum
        print(tup1, tup2)
        return tuple(map(operator.add, tup1, tup2))
    def setAgentLocation(self, location):
        # keeps a record of where the agent is currently located
        self.agentLocation = location
    def getAgentLocation(self):
        return self.agentLocation
    def agentMovement(self, action):
        # Moves the agent
        # gets first coords from action, and adds that to agents current location
        # agent can only make legal moves
        self.setAgentLocation(self.vectorAddition(action[next(iter(action))], self.getAgentLocation()))
    def getLegalMoves(self):
        # 0 is a wall
        # 1 is valid
        moves = self.moves
        legalMoves = {}
        for move in self.moves:
            try:
                newCoords = self.vectorAddition(self.agentLocation, moves[move])
                # checks to see if there is an illegal move
                negativeCoords = True if any(y < 0 for y in newCoords) else False
                outsideMap = True if any(y > len(self.maze[0]) - 1 for y in newCoords) else False
                illegalMove = True if negativeCoords + outsideMap == True else False
                if not illegalMove and newCoords != 0:
                    legalMoves[move] = moves[move]
                    # append to dictionary
                    
            except IndexError as e:
                print("Index error")
                # Not a valid move as it goes out of bounds
                continue
        # returns dictionary of legal moves
        # (0, 0) input
        # {'Up': (1, 0), 'Right': (0, 1)} output
        return legalMoves
# dist = np.sqrt(((a[:, None] - b[:, :, None]) ** 2).sum(0)) 8said animation and ri
m = maze()
a = Qagent.agent(m)
a.run()