class Problem:
	def __init__(self, field, minslice, maxslice):
		self._minslice = minslice * 2
		self._mintype = minslice
		self._maxslice = maxslice
		self._validslices = []
		self._decidevalidslices()
		self._w = len(field[0])
		self._h = len(field)
		self._field = field
		self._tomatoescnt = [[0] * self._w for i in range(self._h)]
		self._mushroomscnt = [[0] * self._w for i in range(self._h)]
		self._filltomatoes()
		self._fillmushrooms()

	def _ismushroom(self, i, j):
		return 1 if self._field[i][j] == 'M' else 0

	def _istomato(self, i, j):
		return self._ismushroom(i, j) ^ 1

	def _filltomatoes(self):
		self._tomatoescnt[0][0] = self._istomato(0, 0)
		for i in range(1, self._h):
			self._tomatoescnt[i][0] += self._istomato(i, 0)
			self._tomatoescnt[i][0] += self._tomatoescnt[i - 1][0]
		for j in range(1, self._w):
			self._tomatoescnt[0][j] += self._istomato(0, j)
			self._tomatoescnt[0][j] += self._tomatoescnt[0][j - 1]
		for i in range(1, self._h):
			for j in range(1, self._w):
				self._tomatoescnt[i][j] += self._istomato(i, j)
				self._tomatoescnt[i][j] += self._tomatoescnt[i][j - 1]
				self._tomatoescnt[i][j] += self._tomatoescnt[i - 1][j]
				self._tomatoescnt[i][j] -= self._tomatoescnt[i - 1][j - 1]

	def _fillmushrooms(self):
		for i in range(self._h):
			for j in range(self._w):
				self._mushroomscnt = (i + 1) * (j + 1) - self._tomatoescnt[i][j]

	def getwidth(self):
		return self._w

	def getheight(self):
		return self._h

	def _gettomatoesonrect(
		self,
		uplefti,
		upleftj,
		height,
		width
		):
		result = self._tomatoescnt[uplefti + height - 1][upleftj + width - 1]
		if(self._valid(uplefti + height - 1, upleftj - 1)):
			result -= self._tomatoescnt[uplefti + height - 1][upleftj - 1]
		if(self._valid(uplefti - 1, upleftj + width - 1)):
			result -= self._tomatoescnt[uplefti - 1][upleftj + width - 1]
		if(self._valid(uplefti - 1, upleftj - 1)):
			result += self._tomatoescnt[uplefti - 1][upleftj - 1]
		return result

	def _getmushroomsonrect(
		self,
		uplefti,
		upleftj,
		height,
		width
		):
		return height * width - self._gettomatoesonrect(uplefti, upleftj, height, width)

	def _decidevalidslices(self):
		for i in range(1, self._maxslice):
			for j in range(1, self._maxslice):
				if(self._minslice <= i * j and i * j <= self._maxslice):
					self._validslices.append((i, j))
		self._validslices.sort(key=lambda n: n[0] * n[1])

	def getvalidslicessizes(self):
		return self._validslices

	def _valid(self, i, j):
		return i >= 0 and i < self._h and j >= 0 and j < self._w

	def isvalidslice(self, uplefti, upleftj, height, width):
		if(not self._valid(uplefti, upleftj)):return False
		if(not self._valid(uplefti + height - 1, upleftj)):return False
		if(not self._valid(uplefti + height - 1, upleftj + width - 1)):return False
		if(not self._valid(uplefti, upleftj + width - 1)):return False

		if(self._gettomatoesonrect(uplefti, upleftj, height, width) < self._mintype):return False
		if(self._getmushroomsonrect(uplefti, upleftj, height, width) < self._mintype):return False

		if((height, width) not in self._validslices):return False

		return True