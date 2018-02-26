from reader import FileReader
from writer import FileWriter, ConsoleWriter
from init_solver import InitSolverSilly, ParallelInitSolver, InitSolverSillyParameterized
from optimize import Tabu
from neighbourhood import Neighbourhood, Neighbourhood_ChangeFormats

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
def scenario_C(file_in, file_out):
    global DEBUG
    reader = FileReader(file_in)
    problem = reader.read()

    init_solver = ParallelInitSolver(InitSolverSillyParameterized, file_output=file_out)
    solution = init_solver.run(problem)
    print("Initial solution score: {}".format(solution.score()))
    if DEBUG:
        solution.print_solution()

    writer = FileWriter(file_out)
    writer.write(solution)


if __name__=="__main__":
    # scenario_A("input_data/example.in", "output_data/example.out")
    # scenario_B("input_data/big.in", "output_data/big.out")
    scenario_C("input_data/small.in", "output_data/small.out")