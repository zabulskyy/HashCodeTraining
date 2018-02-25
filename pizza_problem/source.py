from problem import *
from solver_optim import *
from solution import *
from reader import *

reader = Reader()
p = reader.read()
solv = SolverOptim(p)
solu = solv.run()
solu.out()
print(solu.score())