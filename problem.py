class Problem:
    max_width = 0
    max_height = 0
    L = 0
    H = 0

    field = None
    tomatoes = None
    mushrooms = None
    _slices_formats = None

    def __init__(self, max_height, max_width, L, H):
        self.max_height = max_height
        self.max_width = max_width
        self.L = L
        self.H = H
        self.slices_formats()

        self.field = [[0] * max_width for i in range(max_height)]

        self.tomatoes = [[0] * max_width for i in range(max_height)]
        self.mushrooms = [[0] * max_width for i in range(max_height)]

    def valid(self, i, j):
        return i >= 0 and i < self.max_height and j >= 0 and j < self.max_width

    def is_valid_slice(self, upperi, upperj, height, width):
        if height * width > self.H:
            return False
        if not self.valid(upperi+height-1, upperj+width-1) or not self.valid(upperi, upperj):
            return False
        ts, ms = 0, 0
        for i in range(upperi, upperi+height):
            for j in range(upperj, upperj+width):
                if self.field[i][j] == 'T':
                    ts += 1
                elif self.field[i][j] == 'M':
                    ms += 1

        if ts < self.L or ms < self.L:
            return False

        return True

    def slices_formats(self):
        if not self._slices_formats:
            self._slices_formats = []
            for max_size in range(2*self.L, self.H+1):
                for i in range(1, max_size+1):
                    if max_size % i == 0:
                        self._slices_formats.append((i, max_size // i))
        return self._slices_formats[:]
