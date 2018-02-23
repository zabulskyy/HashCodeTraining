# HashCodeTraining

## Interfaces

Reader(Input File) -> Problem -> Initial Solver -> Solution -> Optimizer 

**class Reader**
*takes care of reading from input file*
- read(input_file): Problem instance

**class Problem**
*represents the problem in memory*

**class Solution**
*represents solution*
- score(): evaluate the solution's score
- is_OK(): returns True if the solution is valid, False in other case
- print(): prints the solution in some managable way
- out(): parse the solution to HashCode output format

**class InitSolver**
*provides some initial solution; there could be a lot of inherited classes*
- run(Problem): returns Solution

**class Optimize**
*continuosly tries to optimize the solutions*
- init(Solution, Problem): initializing
- run(time_limit | iteration_limit): returns best Solution after some number of iterations
