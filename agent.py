import maze as mz
import numpy as np
import random

class agent:
    def __init__(self, maze):
        self.maze = mz.maze()

        # we start at (0,0) and we finish at the very bottom right of the maze
        self.start = (0, 0)
        self.goal = self.maze.getSizeOfMaze()
        
        # the reward table is the size of the maze filled with 0's as data type float 32bit
        #self.rewardsTable = np.zeros(self.maze.getSizeOfMaze(), dtype=np.float32)
        # the rewards table is a dictionary of {state, action, reward}
        # Rewards table should be {"State": {"action": "hello"}}
        # but if we have to do binarysearch after every action, it'll be slower
        # it'll be faster if we replace "state" with the actual state like (0, 0)
        # I think for readability, it would make sense to do it like:
        # {(0, 0): {"State": (0, 0), "Action": (0, 1), "Reward": 0.75}}
        # as we know this small packet is assiocated with (0, 0)
        # 


        # because otherwise,. it would be a list of dictionaries? We can use a dictionary of dictionaries for easy updatinhg. NO! Because where would state be stored lol.
        # We'd want to use a sorted list, sorted on the coordinates to display state.
        # when picking from this table, make sure to pick a legal move!

        # TODO delete this!!
        self.rewardsTable = { (1, 1): {"State": (1, 1), "Action": (0, 1), "Reward": 0.75}, (0, 0): {"State": (0, 0), "Action": (0, 1), "Reward": 0.75}}

        # possible actions
        self.possibleActions = {"Up": (1, 0), "Down": (-1, 0), "Left": (0, -1), "Right": (0, 1)}

        self.gamma = 0.5
        self.learningRate = 0.5

        self.max_epochs = 1000

        self.explore = 0.15
        
        # the agents internal state of the reward
        self.Agentreward = 0.00
        self.penaltyMoving = -0.05

    def qAlgorithm(self, oldValue, reward, maximum):
        """
        oldValue is the old value of the q table value
        reward is how much reward the agent gets, calculated by Reward
        gamma is the discount rate
        maximum is the maximum possible reward from any action the agent can take from its current state
        """
        return oldValue + (self.learningRate * reward + self.gamma * maximum - oldValue)

    def run(self):
        for epoch in range(1, self.max_epochs):
            # a list containing all the steps taken in this epoch
            runCompleted = False
            coords = (0, 0)
            # steps is all the steps it took in the maze
            # as we always start at the self.start position
            steps = [self.start]
            self.Agentreward = 0.00
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
                    legalMoves = self.maze.getLegalMoves()
                    # action, old coords for q table
                    # just need the reward of the movement now!
                    action = random.choice(legalMoves)
                    oldCoords = self.maze.getAgentLocation()
                    # performs the movement
                    self.maze.agentMovement(action)
                    # now we just need to calculate the reward
                    steps.append(oldCoords)
                    # now we need to perform the action
                else:
                    print("yeet no else here yet!")
                



    def reward(self, agentLocation, oldLocation, steps):
        """
        agentLocation = current location of the agent
        oldLocation = previous location of the agent
        Steps = all the steps the agent has taken
        """
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
        
        # updated rewards
        * -0.25 negaticve reward for visting a square it has already been to
        * all squares it visits when it reaches goal gets +1 reward
        * -0.5 reward every time it moves, encourages it to get to end faster
        * Agent keeps internal state of reward it has collected thus far
        
        Game ends when:
        * Agent has -0.5 * 10 (size of maze) points (stops infinite loops / senseless wandering)

        # the rewards table should include the previous state, and the action it took, with the reward gained from it.
        Every time the agent wants to move, it should consult the reward table
        """
        # agent takes a penalty for moving
        totalReward = self.penaltyMoving

        # agent takes a penalty for vising a square it has already been to
        if agentLocation in steps:
            totalReward += -0.25
        
        if agentLocation == self.goal:
            # update all rewards if we've reached the goal
            # TODO can't do this until we have a rewards table!
            totalReward += 1
        # get old reward
        try:
            oldReward = self.rewardsTable[oldLocation]['Reward']
        except KeyError as e:
            # item does not exist in rewards table yet
            oldReward = 0.00
        maximumPossibleReward = self.maximumRewardFromLegalMoves()

        newReward = self.qAlgorithm(oldReward, totalReward, maximumPossibleReward)

        # now we need to calculate maximum mvoement rward from all possible legal moves in this new position
        maximumRewardFromMoves = self.maximumRewardFromLegalMoves()

        # now we need to calculate Q algorithm, and then add +1 to all moves in the reward matrix
    
    def maximumRewardFromLegalMoves(self):
        """
        goes through all legal moves
        calculates maximum possible reward
        needed for Q learning algorithm
        """
        moves = self.maze.getLegalMoves()
        # for every coord in the legal moves
        coords = list(moves.values())
        # set reward of first legal move to max reward
        # prevents bugs
        try:
            maxReward = self.rewardsTable[coords[0]]['Reward']
        except KeyError as e:
            maxReward = 0.00
        for i in list(moves.values()[1::]):
            try:
                newReward = self.rewardsTable[i]['Reward']
            except KeyError as e:
                newReward = 0.00
            if maxReward < newReward:
                maxReward = newReward
        return maxReward


        

        return "No return yet"
    def sortRewardsTable(self):
        # sorts the rewards table on state
        # so logically, coordinates (0, 0) comes first
        newlist = sorted(x, key=lambda k: k['State'])

    def searchRewardsTable(self, oldCoords, newCoords):
        # Searches the rewards table, returns the item. 
        # if we can search instantly,. this function is not needed.
        return None



    