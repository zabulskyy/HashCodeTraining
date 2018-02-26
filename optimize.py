from solution import Solution
from problem import Problem

import time
import os
import queue
import multiprocessing as mp

MAX_ITERATION = 1000
TABU_LIST_LENGTH = 100

class Optimizer:
    """
    Abstract optimizer class
    Uses some Neighbourhood classes to search in for the solutions' neighbours
    """
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
    """
    Classical tabu search
    """

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


class ParallelTabu(Optimizer):
    """
    Parallel tabu search
    Runs parallel tabu searches for the topmost candidates
    """

    tabu_limit = 100

    def run_instance(self, id, solution, n_process):
        neighbours = self.neighbourhood.get_neighbours(solution)
        result = [(neighbour, neighbour.score(), neighbour.get_hash()) for neighbour in neighbours]
        result.sort(key=lambda x: x[1], reverse=True)
        return result[:n_process]

    def run(self, time_limit=float('inf'), n_process=None):
        """
        :param time_limit: Time limit (lower bound) in seconds for the procedure to work
        :param n_process: Number of parallel processes to use
        :return:
        """
        end_time = time.time() + time_limit
        self.neighbourhood = self.Neighbourhood_Class(self.p)
        best_candidate = self.s
        best_score = self.s.score()
        hash = best_candidate.get_hash()
        candidates = [(best_candidate, best_score, hash)]
        super_candidate = best_candidate
        tabu_list = [hash]

        if not n_process:
            n_process = os.cpu_count()

        while time.time() < end_time:
            if self.debug:
                print("Tabu len: {}. Best candidates score".
                      format(len(tabu_list)), [c[1] for c in candidates[:min(n_process, len(candidates))]])

            results = []
            pool = mp.Pool(n_process)
            id = 1
            for candidate in candidates[:min(n_process, len(candidates))]:
                res = pool.apply_async(func=self.run_instance, args=(id, candidate[0], n_process, ))
                results.append(res)
                id += 1
            pool.close()
            pool.join()

            new_candidates = []
            for res in results:
                new_candidates += [c for c in res.get() if c[2] not in tabu_list]
            tabu_list += [c[2] for c in new_candidates]
            if self.debug:
                print("Amount of new candidates: {}".format(len([c[2] for c in new_candidates])))
            new_candidates.sort(key=lambda x: x[1], reverse=True)

            if new_candidates and new_candidates[0][1] > best_score:
                best_score = new_candidates[0][1]
                super_candidate = new_candidates[0][0]
                if self.debug:
                    print("New best score: ", best_score)

            if len(new_candidates)<n_process:
                candidates = candidates[:min(n_process-len(new_candidates), len(candidates))] + new_candidates
            else:
                candidates = new_candidates

            while len(tabu_list) > self.tabu_limit:
                tabu_list.pop(0)

        return super_candidate