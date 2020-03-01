import maze as mz
import numpy as np
import random

class agent:
    def __init__(self, maze):
        this.maze = mz.maze()

        # we start at (0,0) and we finish at the very bottom right of the maze
        self.start = (0, 0)
        self.goal = self.maze.getSizeOfMaze()
        
        # the reward table is the size of the maze filled with 0's as data type float 32bit
        self.rewardsTable = np.zeros(self.maze.getSizeOfMaze(), dtype=np.float32)

        # possible actions
        self.possibleActions = {"Up": (1, 0), "Down": (-1, 0), "Left": (0, -1), "Right": (0, 1)}

        self.gamma = 0.5
        self.learningRate = 0.5

        self.max_epochs = 1000

        self.explore = 0.15

    def qAlgorithm(oldValue, learningRate, reward, gamma, maximum):
        """
        oldValue is the old value of the q table value
        reward is how much reward the agent gets, calculated by Reward
        gamma is the discount rate
        maximum is the maximum possible reward from any action the agent can take from its current state
        """
        return oldValue + (learningRate * reward + gamma * maximum - oldValue)
    def run():
        for epoch in range(1, self.max_epochs):
            # a list containing all the steps taken in this epoch
            runCompleted = False
            coords = (0, 0)
            steps = []
            while not runCompleted:
                # if we are at the goal, our run is completed!!!
                if coords == self.goal:
                    runCompleted = True
                    break
                
                # 99 because 0 to 15 is 16 numbers (16% chance)
                exploreOrNot = True if random.random(0, 99) < self.explore else False
                if exploreOrNot:
                    # need to choose legal moves
                    # randomy choose an action to take
                    action = random.choice(list(self.possibleActions.keys()))




    def reward(coordinates):
        """
        if i record path it takes to get to the end result
        then once it reaches the end, i can update the q learning table to reflect this
        exploration means it will still go weird ways
        but it'll have to explore more than usual. normally q learning tables update after every action
        Unless every action incurs a penalty, but reaching the reward means that path is rewarded?

        ok so what if we take the coordinates, add them together (1, 1) = 2, then divide by 10 + 10?
        that way, the agent is continually moving "towards" the goal
        then we simply add the reward onto the path for the agent reaching the goal

        we need to make the agent choose the maximum goal at each point

        reward has to be added after each goal, otherwise we could just do the entire table right at the start
        
        agent takes a negative penality if it already visits a square it has been to
        maybe the agent itself should have a reward function, it takes negative reward for visiting squares its already been to
        and positive reward 

        -0.25 negative reward for visitng a square its already been to, 

        To avoid infinite loops and senseless wandering, the game is ended (**lose**) once the total reward of the rat is below the negative threshold: (-0.5 * maze.size). We assume that under this threshold, the rat has "lost its way" and already made too many errors from which he has learned enough, and should proceed to a new fresh game. 
        
        ok we have a dict of (coords, action) with a reward
        if agent goes outside 

        Each move has a reward.
        The max rewards of 1 point is given when the agent reaches the goal
        Penialised -0.25 for any move to a cell it has already visited
        -0.05 reward for every time it moves, encourages it to get to the end faster
        game ends when agent has -0.5 * 10 (size of maze) points

        Eventually, the best path to the maze will be the one which incurs the least penalty after having explored the entire maze.
        """
        return sum(coordinates) / sum(self.goal))



    