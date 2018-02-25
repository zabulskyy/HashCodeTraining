from problem import Problem
from solution import Solution


class SolverOptim:
	def __init__(self, problem):
		self.p = problem

		n = self.p.getheight()
		m = self.p.getwidth()
		
		self.occupied = [[False] * m for i in range(n)]
		self.solutionfield = [[(0,0)] * m for i in range(n)]

	def run(self):
		n = self.p.getheight()
		m = self.p.getwidth()
		
		maxslice = [[0] * m for i in range(n)]

		for i in range(n):
			for j in range(m):
				current = 0
				for currentslice in self.p.getvalidslicessizes():
					if(not self.p.isvalidslice(i, j, currentslice[0], currentslice[1])):
						continue
					if(self.check(i, j, currentslice[0], currentslice[1])):
						continue
					current = max(current, currentslice[0] * currentslice[1])
				maxslice[i][j] = current

		data = {}
		datalst = []
		for i in range(n):
			for j in range(m):
				cell = (i, j)
				for currentslice in self.p.getvalidslicessizes():
					if(not self.p.isvalidslice(i, j, currentslice[0], currentslice[1])):
						continue
					if(not self.check(i, j, currentslice[0], currentslice[1])):
						continue
					score = currentslice[0] * currentslice[1]

					alternative = 0

					for ti in range(currentslice[0]):
						for tj in range(currentslice[1]):
							if(ti == 0 and tj == 0):continue
							alternative += maxslice[i + ti][j + tj]
					score -= alternative
					data[(cell, currentslice)] = score
					datalst.append((cell, currentslice))

		datalst.sort(key = lambda n: data[n], reverse=True)

		for item in datalst:
			cell, currentslice = item
			if(not self.check(cell[0], cell[1], currentslice[0], currentslice[1])):
				continue
			self.put(cell[0], cell[1], currentslice[0], currentslice[1])

		return Solution(self.p, self.solutionfield)

	def put(self, uplefti, upleftj, height, width):
		for i in range(height):
			for j in range(width):
				self.occupied[i + uplefti][j + upleftj] = True
		self.solutionfield[uplefti][upleftj] = (height, width)
	def check(self, uplefti, upleftj, height, width):
		for i in range(height):
			for j in range(width):
				if(self.occupied[i + uplefti][j + upleftj]):
					return False
		return True
