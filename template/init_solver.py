from solution import Solution
from writer import FileWriter

from multiprocessing import Pool


class InitSolver:

    def __init__(self):
        pass

    def run(self, problem):
        """
        @type problem: Problem
        :rtype: Solution
        """
        raise Exception("Need to implement 'run' method")

    @staticmethod
    def parameters_universum_set():
        return []


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


class ParallelInitSolver(InitSolver):

    problem = None
    slave_solver = None
    n_process = None

    def __init__(self, slave_solver, number_of_processes=None, file_output=None):
        """
        @:param number_of_processes: if None then will be equal to the number of CPUs
        """
        self.slave_solver = slave_solver
        self.n_process = number_of_processes
        self.file_output = file_output

    def run_instance(self, id, parameters):
        init_solver = self.slave_solver(parameters)
        solution = init_solver.run(self.problem)
        score = solution.score()
        print("ID: {}. Initial solution score: {}, parameters: {}".
              format(id, score, ", ".join(["{}: {}".format(k, v) for k, v in parameters.items()])))

        if self.file_output:
            writer = FileWriter("{}.{}".format(self.file_output, id))
            writer.write(solution)

        return solution, score

    def run(self, problem):
        """
        @type problem: Problem
        :rtype: Solution
        """
        self.problem = problem
        parameters = self.slave_solver.parameters_universum_set()
        results = []

        with Pool(processes=self.n_process) as pool:
            id = 1
            for par in parameters:
                res = pool.apply_async(func=self.run_instance, args=(id, par,))
                results.append(res)
                id += 1
            pool.close()
            pool.join()

        all_scores = [res.get() for res in results]
        best_solution, best_score = max(all_scores, key=lambda x: x[1])
        return best_solution
