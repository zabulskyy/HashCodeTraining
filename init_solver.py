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
# Goes from left to right, from top to bottom
# Cut slice whenever max conditions are met (<=H pices in a slice)
#
class InitSolverSilly(InitSolver):

    def run(self, problem):
        """
        @type problem: Problem
        :rtype: Solution
        """
        sol = Solution(problem)     # type: Solution
        formats = problem.slices_formats()
        row, col = 0, 0
        while True:
            for f in formats:
                if sol.is_free_space(row, col, f[0], f[1]) and problem.is_valid_slice(row, col, f[0], f[1]):
                    sol.create_new_slice(row, col, f[0], f[1])
                    col += f[1]
                    break
            else:
                col += 1
            if col>=problem.max_width:
                row += 1
                col = 0
            if row>=problem.max_height:
                break
            # print(row, col)
        return sol


class InitSolverSillyParameterized(InitSolver):

    direction = 0
    formats_order_desc = False
    formats_quadratic_first = False

    def __init__(self, parameters={}):
        self.direction = parameters.get('direction', 0)
        self.formats_order_desc = parameters.get('formats_order_desc', False)
        self.formats_quadratic_first = parameters.get('formats_quadratic_first', False)

    @staticmethod
    def parameters_universum_set():
        result = []
        for direction in range(4):
            for formats_order_desc in [False, True]:
                for formats_quadratic_first in [False, True]:
                    result.append({'direction': direction,
                                   'formats_order_desc': formats_order_desc,
                                   'formats_quadratic_first': formats_quadratic_first})
        return result

    def run(self, problem):
        """
        @type problem: Problem
        :rtype: Solution
        """
        sol = Solution(problem)     # type: Solution
        formats = problem.slices_formats()      # type: list[(int,int)]
        formats.sort(key=lambda x: abs(x[0]-x[1]) if self.formats_quadratic_first else x[0]*x[1], reverse=self.formats_order_desc)

        if self.direction==0:       # from upper left to bottom right
            row, col, row_add, col_add = 0, 0, 1, 1
        elif self.direction==1:     # from upper right to bottom left
            row, col, row_add, col_add = 0, problem.max_width-1, 1, -1
        elif self.direction==2:     # from bottom left to upper right
            row, col, row_add, col_add = problem.max_height-1, 0, -1, 1
        elif self.direction==3:     # from bottom right to upper left
            row, col, row_add, col_add = problem.max_height-1, problem.max_width-1, -1, -1

        while True:
            for f in formats:
                x = row if row_add==1 else row - f[0]
                y = col if col_add == 1 else col - f[1]
                if sol.is_free_space(x, y, f[0], f[1]) and problem.is_valid_slice(x, y, f[0], f[1]):
                    sol.create_new_slice(x, y, f[0], f[1])
                    col += f[1] * col_add
                    break
            else:
                col += col_add
            if (col_add==1 and col>=problem.max_width) or (col_add==-1 and col<0):
                row += row_add
                col = 0 if col_add==1 else problem.max_width-1
            if (row_add==1 and row>=problem.max_height) or (row_add==-1 and row<0):
                break
            # print(row, col)
        return sol


class InitSolverGreedy(InitSolver):

    def run(self, problem):
        """
        @type problem: Problem
        :rtype: Solution
        """
        raise Exception("Need to implement 'run' method")


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
        print("Initial solution score: {}, parameters: {}".
              format(score, ", ".join(["{}: {}".format(k, v) for k, v in parameters.items()])))

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
        print("Best score: {}".format(best_score))
        return best_solution
