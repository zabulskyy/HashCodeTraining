from problem import Problem
from solution import Solution


class SolverNaive:
	def __init__(self, problem):
		self.p = problem

		n = self.p.getheight()
		m = self.p.getwidth()
		
		self.occupied = [[False] * m for i in range(n)]
		self.solutionfield = [[(0,0)] * m for i in range(n)]

	def run(self):
		n = self.p.getheight()
		m = self.p.getwidth()
		result = [[0] * m for i in range(n)]
		for i in range(n):
			for j in range(m):
				for item in self.p.getvalidslicessizes():
					if(self.p.isvalidslice(i, j, item[0], item[1])):
						result[i][j] += 1

		cells = []
		for i in range(n):
			for j in range(m):
				if(result[i][j] > 0):
					cells.append((i, j))
		cells.sort(key=lambda n: result[n[0]][n[1]])

		for cell in cells:
			uplefti, upleftj = cell
			for slicepice in self.p.getvalidslicessizes():
				if(not self.p.isvalidslice(uplefti, upleftj, slicepice[0], slicepice[1])):
					continue
				if(not self.check(uplefti, upleftj, slicepice[0], slicepice[1])):
					continue
				self.put(uplefti, upleftj, slicepice[0], slicepice[1])
				break

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
