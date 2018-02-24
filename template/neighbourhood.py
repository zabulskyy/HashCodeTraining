from problem import Problem
from solution import Solution

import random

class Neighbourhood:
    """
    Abstract class for the neighbourhood search
    """

    s = None
    p = None

    def __init__(self, problem):
        self.p = problem    # type: Problem

    def get_neighbours(self, solution):
        """
        Generates neighbouring solutions for the provided solution
        :param solution:
        :rtype: list[Solution]
        """
        return []
