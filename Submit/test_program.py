import Qagent
import numpy as np
import maze
m = maze.maze()

def test_q_algorithm_normal():
    """
    Testing to see if the q algorithm operates correctly
    """
    q = Qagent.agent(m)
    result = q.qAlgorithm(0.54, 1, 0.67)
    assert result == 0.835

def test_q_algorithm_negative():
    """
    Testing to see if it breaks on negative
    """
    q = Qagent.agent(m)
    result = q.qAlgorithm(-50000, 60, 0.9999999)
    assert result > 1

def test_q_algorithm_big():
    """
    Testing to see if it breaks on large numbers
    """
    q = Qagent.agent(m)
    result = q.qAlgorithm(500000000000000000000000000000000000000000000000000, 500000000000000000000000000000000000000000000000000, 500000000000000000000000000000000000000000000000000)
    assert result > 1

def test_q_algorithm_zero():
    """
    Testing to see if it breaks on 0 input
    """
    q = Qagent.agent(m)
    result = q.qAlgorithm(0, 0, 0)
    assert result == 0.0