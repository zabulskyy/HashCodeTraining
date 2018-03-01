from reader import FileReader
from writer import FileWriter, ConsoleWriter
from init_solver import InitSolverSilly, ParallelInitSolver, InitSolverSillyParameterized
from optimize import Tabu, ParallelTabu
from neighbourhood import Neighbourhood, Neighbourhood_ChangeFormats

from optparse import OptionParser

DEBUG = False

def scenario_A(file_in, file_out):
    global DEBUG
    reader = FileReader(file_in)
    problem = reader.read()

    init_solver = InitSolverSilly()
    solution = init_solver.run(problem)
    print("Initial solution score: {}".format(solution.score()))
    if DEBUG:
        solution.print_solution()

    writer = FileWriter(file_out)
    writer.write(solution)

def scenario_B(file_in, file_out):
    global DEBUG
    reader = FileReader(file_in)
    problem = reader.read()

    init_solver = InitSolverSilly()
    solution = init_solver.run(problem)
    print("Initial solution score: {}".format(solution.score()))
    if DEBUG:
        solution.print_solution()

    optimizer = Tabu(problem, solution, Neighbourhood_ChangeFormats, debug=True)
    optimized_solution = optimizer.run(time_limit=100)

    print("optimized solution score: {}".format(optimized_solution.score()))
    if DEBUG:
        optimized_solution.print_solution()

    writer = FileWriter(file_out)
    writer.write(optimized_solution)


# Parallel initial solver
def scenario_C(file_in, file_out, file_par=None):
    global DEBUG
    reader = FileReader(file_in)
    problem = reader.read()

    init_solver = ParallelInitSolver(InitSolverSillyParameterized, file_output=file_out)
    solution = init_solver.run(problem, file_par)
    print("Initial solution score: {}".format(solution.score()))
    if DEBUG:
        solution.print_solution()

    writer = FileWriter(file_out)
    writer.write(solution)


# Parallel initial solver & parallel tabu search
def scenario_D(file_in, file_out, file_par=None):
    global DEBUG
    reader = FileReader(file_in)
    problem = reader.read()

    init_solver = ParallelInitSolver(InitSolverSillyParameterized, file_output=file_out)
    solution = init_solver.run(problem, file_par)
    print("Initial solution score: {}".format(solution.score()))
    if DEBUG:
        solution.print_solution()

    optimizer = ParallelTabu(problem, solution, Neighbourhood_ChangeFormats, debug=True)
    optimized_solution = optimizer.run(time_limit=1000)

    print("optimized solution score: {}".format(optimized_solution.score()))
    if DEBUG:
        optimized_solution.print_solution()

    writer = FileWriter(file_out)
    writer.write(solution)

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-i", "--input-file", dest="in_file", help="Input file name", metavar="FILE")
    parser.add_option("-o", "--output-file", dest="out_file", help="Output file name", metavar="FILE")
    parser.add_option("-p", "--param-file", dest="par_file", help="Parameters' file name", metavar="FILE", default=None)
    (options, args) = parser.parse_args()

    print(options.in_file, options.out_file, options.par_file)

    scenario_C(options.in_file, options.out_file, options.par_file)

    # scenario_A("input_data/example.in", "output_data/example.out")
    # scenario_B("input_data/big.in", "output_data/big.out")
    # scenario_C("input_data/medium.in", "output_data/medium.out")
    # scenario_D("input_data/medium.in", "output_data/medium.out")