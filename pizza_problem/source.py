from problem import *
from solver import *
from solution import *
from reader import *

reader = Reader()
p = reader.read()
solv = SolverNaive(p)
solu = solv.run()
solu.out()
print(solu.score())