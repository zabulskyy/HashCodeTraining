from problem import *
from solver import *
from solution import *

p = Problem(["MMT", "TTT", "MTM"], 1, 4)
solv = SolverNaive(p)
solu = solv.run()

print(solu.score())