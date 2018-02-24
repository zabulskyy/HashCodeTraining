from problem import Problem
from copy import deepcopy

import random
import hashlib

class Solution:
    """
    Represents a solution for the problem
    """

    def __init__(self, problem):
        self.p = problem    # type: Problem
        # TODO: Add your solution objects

    def score(self):
        """
        Calculates solution's score
        """
        score = 0
        # TODO: Add score calculation
        return score

    def is_OK(self):
        """
        Checks whether the solution is valid
        :return: Boolean, Message
        """
        return True, "Solution is valid!"

    def print_solution(self):
        """
        Prints solution in a readable form
        """
        raise Exception("Need to implement 'print_solution' method")

    def get_hash(self, is_string=False):
        """
        Calculates a hash-string to use later for hashing different solutions
        :param is_string: Boolean. Set to True to have a hash in string form
        """
        m = hashlib.md5()   # Also may use hashlib.sha256

        # TODO: write your hashing
        # hash_str = ...

        m.update(hash_str)
        if is_string:
            return m.hexdigest()
        return m.digest()

    def duplicate(self):
        """
        Creates a duplicate of the current solution
        :rtype: Solution
        """
        s = Solution(self.p)
        # TODO: Add copying of all solution's structures
        return s