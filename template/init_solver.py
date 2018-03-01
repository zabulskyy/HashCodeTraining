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

        Example of the parameter file:
        # Some comment
        par1= 100
          par2=-2;      par3="asdfsaf";     par4 = false;   par5=TRUE;  par6=False; par7=-5.10
        par1=1,2; par2="abc","xyz"; par3=True,False
        par1=1:5; par2=-6:6:3

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
            writer = FileWriter("{}.{}.{}.out".format(self.file_output, id, score))
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
        return best_solution
