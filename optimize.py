from solution import Solution
from problem import Problem
from writer import ConsoleWriter

import time

MAX_ITERATION = 1000
TABU_LIST_LENGTH = 100

class Optimizer:
    s = None
    p = None

    def __init__(self, problem, solution, Neighbourhood_Class, debug=False):
        self.s = solution       # type: Solution
        self.p = problem        # type: Problem
        self.debug = debug
        self.Neighbourhood_Class = Neighbourhood_Class

    def run(self, time_limit=float('inf')):
        raise Exception("Need to implement 'run' method")

class Tabu(Optimizer):

    tabu_limit = 100

    def run(self, time_limit=float('inf')):
        tabu_list = []

        end_time = time.time() + time_limit
        n = self.Neighbourhood_Class(self.p)
        best_candidate = self.s
        super_candidate = best_candidate

        best_score = self.s.score()
        while time.time() < end_time:
            # check all neighbours
            neighbours = n.get_neighbours(best_candidate)
            best_candidate_score = 0
            for neighbour in neighbours:
                # neighbour.print_solution()
                neighbour_key = neighbour.get_hash()
                neighbour_score = neighbour.score()
                if not neighbour_key in tabu_list and neighbour_score > best_candidate_score:
                    best_candidate_score = neighbour_score
                    best_candidate = neighbour

            if best_candidate_score > best_score:
                if self.debug:
                    print("New best score: ", best_candidate_score)
                    # best_candidate.print_solution()
                    # writer = ConsoleWriter()
                    # writer.write(best_candidate)
                best_score = best_candidate_score
                super_candidate = best_candidate

            tabu_list.append(best_candidate.get_hash())

            if len(tabu_list) > self.tabu_limit:
                tabu_list.pop(0)

        return super_candidate