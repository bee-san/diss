import Qagent
import numpy as np
import maze


def test_maze_movement():
    """ Testing the movement of the agent
    in the maze"""
    m = maze.maze()
    # move to the right starting at 0,0 
    result = m.vectorAddition((0, 1), m.getAgentLocation())
    assert result == (0, 1)