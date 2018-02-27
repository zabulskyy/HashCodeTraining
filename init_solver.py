from solution import Solution
from writer import FileWriter

from multiprocessing import Pool
import re


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
    def parameters_universum():
        return []

    @staticmethod
    def parameters_universum_from_file(file_name):
        """
        Reads parameters from file and generate all allowed permutations.
         The type of lines that are prohibited:
         - starts with '#' or ';' - comment
         - each line consists of several parameter sections separated by semicolon ';'
         - each parameter section consists of parameter name and value section separated by equal sign '='
         - parameter name may include latin letters, digits, '-', '_'
         - no spaces are allowed in parameter names
         - each value section can be one of the following:
         -- concrete value: number (int or float), string in quotes or doublequotes, boolean constants (True, False)
         -- list of values separated by comma ','
         -- range for the number values in one of two possible formats:
            - A:B will generate a set of numbers from A to B included (e.g. 1:5 => 1, 2, 3, 4, 5)
            - A:B:C will generate a set of number from A to B with the step C (e.g. -6:6:3 => -6, -3, 0, 3, 6)

        :param file_name: Input text file
        :return: list of parameter dicts
        """
        parameters = []
        with open(file_name, 'r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.replace('\n', '')
            if not line or line[0] == '#' or line[0] == ';':  # skip a commented line
                continue
            new_pars, cardinals = {}, {}
            chunks = re.split('[\t;]', line)
            for chunk in chunks:
                m = re.fullmatch('\s*([\w\d_-]+)\s*=(.+)$', chunk)
                if not m:
                    continue
                par_name = m.group(1)
                par_values = list(map(str.strip, m.group(2).split(',')))
                par_values_list = []
                for value in par_values:
                    m = re.fullmatch('^[\'"](.+)[\'"]$', value)
                    if m:
                        par_values_list.append(m.group(1))
                        continue
                    if value.lower() == 'true':
                        par_values_list.append(True)
                        continue
                    elif value.lower() == 'false':
                        par_values_list.append(False)
                        continue
                    rng = value.split(':')
                    convert = lambda x: float(x) if x.find('.') >= 0 else int(x)
                    if len(rng) == 1:
                        par_values_list.append(convert(rng[0]))
                    elif len(rng) == 2:
                        par_values_list += [convert(rng[0]) + i for i in
                                            range(int(convert(rng[1]) - convert(rng[0])) + 1)]
                    elif len(rng) >= 3:
                        a, b, d = convert(rng[0]), convert(rng[1]), convert(rng[2])
                        while a <= b:
                            par_values_list.append(a)
                            a += d
                new_pars[par_name] = par_values_list
                cardinals[par_name] = [len(par_values_list), 0]  # get cardinal number of a value set for each parameter

            keys = new_pars.keys()
            while True:
                parameters.append({k: new_pars[k][v[1]] for k, v in cardinals.items()})
                for k in keys:
                    cardinals[k][1] += 1
                    if cardinals[k][1] == cardinals[k][0]:
                        cardinals[k][1] = 0
                    else:
                        break
                else:
                    break

        return parameters

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
            if col >= problem.max_width:
                row += 1
                col = 0
            if row >= problem.max_height:
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
    def parameters_universum():
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

    def run(self, problem, parameters_file=None):
        """
        @type problem: Problem
        :rtype: Solution
        """
        self.problem = problem
        if parameters_file:
            parameters = self.slave_solver.parameters_universum_from_file(parameters_file)
        else:
            parameters = self.slave_solver.parameters_universum()
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
