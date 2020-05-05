import numpy as np
import random

class agent:
    def __init__(self, maze):
        self.maze = maze

        # Where does the agent start>
        self.start = (0, 0)

        # Where is the goal of the agent?
        # self.maze.getSizeOfMaze() sets the agent goal to the very bottom right hand corner
        # Can use coordinates such as (15, 15)
        self.goal = self.maze.getSizeOfMaze()
        
        # The reward table the agent starts with. You can manually insert rewards like:
        # self.rewardsTable = { (1, 1): {"State": (1, 1), "Action": (0, 1), "Reward": 0.75}, (0, 0): {"State": (0, 0), "Action": (0, 1), "Reward": 0.75}}
        self.rewardsTable = {}

        # What actions can the agent take?
        self.possibleActions = {"Up": (1, 0), "Down": (-1, 0), "Left": (0, -1), "Right": (0, 1)}

        # How much the agent expects to gain from future value.
        self.gamma = 0.5

        # How fast can the agent learn?
        self.learningRate = 0.5

        # How many times will the agent complete the maze before it stops?
        self.max_epochs = 1000

        # The probability that the agent will explore on that round, instead of exploiting the rewards table
        self.explore = 0.15
        
        # The agents current reward when it starts
        self.Agentreward = 0.00

        # The agents penalty for moving. Prevents the agent from running around in circles
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
                    # agent gets 1 for completing the reward
                    for i in steps:
                        rwrd = self.finalReward(i)
                        self.rewardsTable[i] = {"State": i, "Action": self.rewardsTable[i]["Action"], "Reward": rwrd}
                    break
                
                # 99 because 0 to 15 is 16 numbers (16% chance)
                exploreOrNot = True if random.randint(0, 99) < self.explore else False
                if exploreOrNot:
                    # need to choose legal moves
                    # randomy choose an action to take
                    legalMoves = self.maze.getLegalMoves()
                    # action, old coords for q table
                    # just need the reward of the movement now!
                    action = random.choice(list(legalMoves.values()))
                    oldCoords = self.maze.getAgentLocation()
                    # performs the movement
                    self.maze.agentMovement(action)
                    # now we just need to calculate the reward
                    steps.append(oldCoords)
                    # now we need to add the reward to the table.
                    newReward = self.reward(self.maze.getAgentLocation(), oldCoords, steps)
                    self.rewardsTable[oldCoords] = {"State": oldCoords, "Action": action, "Reward": newReward}
                    # self.rewardsTable = { (1, 1): {"State": (1, 1), "Action": (0, 1), "Reward": 0.75}, (0, 0): {"State": (0, 0), "Action": (0, 1), "Reward": 0.75}}
                else:
                    move = self.bestMove()
                    oldCoords = self.maze.getAgentLocation()

                    self.maze.agentMovement(move)

                    steps.append(oldCoords)

                    newReward = self.reward(self.maze.getAgentLocation(), oldCoords, steps)

                    self.rewardsTable[oldCoords] = {"State": oldCoords, "Action": move, "Reward": newReward}


                
    def finalReward(self, location):
    

        totalReward = 1
        try:
            oldReward = self.rewardsTable[location]['Reward']
        except KeyError as e:
            oldReward = 0.00
        maximumPossibleReward = 1
        newReward = self.qAlgorithm(oldReward, totalReward, maximumPossibleReward)
        
        return newReward

    def reward(self, agentLocation, oldLocation, steps):
        """
        agentLocation = current location of the agent
        oldLocation = previous location of the agent
        Steps = all the steps the agent has taken

        Record the path the agent takes to get to the end result, once it reaches the end we can update the Q learning table to reflect this.
        Reaching the reward means that path incurs a reward of 1, but each action also generates a reward.
        To generate this reward, we use the Q learning algorithm.

        To do that, we need to do a few things:
        * The agent chooses the maximum reward at each point that is exploitationary
        * Reward is added after each action
        
        But this doesn't solve the issue of the agent mindlessly wandering. 

        We can apply a negative reward to the agent to prevent this. 

        But again, this doesn't solve the problem - the agent just gets a lower reward.

        We have another problem - the agent may choose to revisit squares it has already been to.

        Therefore, the agent takes a negative reward when visiting a square it has been to.

        To avoid infinite loops and mindless wandering, it is not enough that the agent takes negative reward. The game should end (the agent loses)
        when the total reward is below a negative threshold. We assume that when the agent reaches this threshold, it has lost its way and already has made too
        many errors from which the agent has learned enough. The agent should start a fresh new game.

        Eventually, the best path to the maze will be the one which incurs the least penalty after having explored the entire maze (or the highest reward).

        The rough numbers I should use are:
        
        # updated rewards
        * -0.25 negative reward for visting a square it has already been to
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

        # now we need to calculate Q algorithm, and then add +1 to all moves in the reward matrix. We can do this in the main code me thinks?
        return newReward
    
    def bestMove(self):
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
            bestMove = self.rewardsTable[coords[0]]['Action']
        except KeyError as e:
            maxReward = 0.00
            # chooses first move as the best
            bestMove = moves[next(iter(moves))]
        # iterates over the dictionary
        for key, i in moves.values():    
            try:
                newReward = self.rewardsTable[i]['Reward']
            except KeyError as e:
                newReward = 0.00
            if maxReward < newReward:
                maxReward = newReward
                bestMove = i # best move equal to the best move we should do, which is i as the data is {'Up': (1, 0)}
        return bestMove
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
        for i in list(moves.values())[1::]:
            try:
                newReward = self.rewardsTable[i]['Reward']
            except KeyError as e:
                newReward = 0.00
            if maxReward < newReward:
                maxReward = newReward
        return maxReward
