# Class Templates

Basic interfaces

**class Reader**
*takes care of reading from input file or console*
- read(): returns Problem instance

**class Writer**
*takes care of writing a solution to output file or console*
- write(): writes Solution

**class Problem**
*represents the problem in memory*

**class Solution**
*represents solution*
- score(): evaluate the solution's score
- is_OK(): returns True if the solution is valid, False in other case
- print_solution(): prints the solution in some managable way
- duplicate(): makes a copy of the solution
- get_hash(): calculates a hash string for the solution

**class InitSolver**
*provides some initial solution; there could be a lot of inherited classes*
- run(Problem): returns Solution

**class Optimize**
*continuosly tries to optimize the solutions*
- init(Solution, Problem): initializing
- run(time_limit | iteration_limit): returns best Solution after some number of iterations

**class Neighbourhood**
*generates neighbour solutions; needed for the optimization techniques*
- get_neighbours(Solution):
