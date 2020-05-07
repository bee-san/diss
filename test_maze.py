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

def test_maze_movement_up():
    """ Testing the movement of the agent
    in the maze"""
    m = maze.maze()
    # move to the right starting at 0,0 
    result = m.vectorAddition((1, 0), m.getAgentLocation())
    
    assert result == (1, 0)

def test_maze_movement_legal_moves():
    """ Does legal moves work?"""
    m = maze.maze()
    # move to the right starting at 0,0 
    result = m.getLegalMoves()
    
    assert True if "Right" in result else False