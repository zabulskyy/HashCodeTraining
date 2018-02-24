from problem import Problem
from solution import Solution

class InitSolver:

    def __init__(self):
        pass

    def run(self, problem):
        """
        @type problem: Problem
        :rtype: Solution
        """
        raise Exception("Need to implement 'run' method")

#
# Some silly implementation
#
class InitSolverSilly(InitSolver):

    def run(self, problem):
        """
        @type problem: Problem
        :rtype: Solution
        """
        sol = Solution(problem)     # type: Solution

        # TODO: Add your solution process here

        return sol