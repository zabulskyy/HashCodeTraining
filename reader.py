from problem import Problem

class Reader:
    def __init__(self):
        pass

    def filltomatoes(self, p):
        p.tomatoes[0][0] = 1 if p.field[0][0] == 'T' else 0
        for i in range(1, p.max_height):
            p.tomatoes[i][0] = 1 if p.field[i][0] == 'T' else 0
            p.tomatoes[i][0] += p.tomatoes[i - 1][0]
        for j in range(1, p.max_width):
            p.tomatoes[0][j] = 1 if p.field[0][j] == 'T' else 0
            p.tomatoes[0][j] += p.tomatoes[0][j - 1]
        for i in range(1, p.max_height):
            for j in range(1, p.max_width):
                p.tomatoes[i][j] = 1 if p.field[i][j] == 'T' else 0
                p.tomatoes[i][j] += (p.tomatoes[i - 1][j] + p.tomatoes[i][j - 1] - p.tomatoes[i - 1][j - 1])

    def fillmushrooms(self, p):
        p.mushrooms[0][0] = 1 if p.field[0][0] == 'M' else 0
        for i in range(1, p.height):
            p.mushrooms[i][0] = 1 if p.field[i][0] == 'M' else 0
            p.mushrooms[i][0] += p.mushrooms[i - 1][0]
        for j in range(1, p.width):
            p.mushrooms[0][j] = 1 if p.field[0][j] == 'M' else 0
            p.mushrooms[0][j] += p.mushrooms[0][j - 1]
        for i in range(1, p.height):
            for j in range(1, p.width):
                p.mushrooms[i][j] = 1 if p.field[i][j] == 'M' else 0
                p.mushrooms[i][j] += (p.mushrooms[i - 1][j] + p.mushrooms[i][j - 1] - p.mushrooms[i - 1][j - 1])

    def read(self):
        raise Exception("Need to implement 'read' method")

class ConsoleReader(Reader):
    def read(self):
        n, m, l, h = map(int, input().split())
        p = Problem(n, m, l, h)
        for i in range(n):
            row = input()
            for j in range(m):
                p.field[i][j] = row[j]
        self.fillmushrooms(p)
        self.filltomatoes(p)
        return p

class FileReader(ConsoleReader):
    def __init__(self, file_name):
        ConsoleReader.__init__(self)
        self.file_name = file_name

    def read(self):
        with open(self.file_name,'r') as f:
            n, m, l, h = map(int, f.readline().split())
            p = Problem(n, m, l, h)
            for i in range(n):
                row = f.readline()
                for j in range(m):
                    p.field[i][j] = row[j]
            # self.fillmushrooms(p)
            # self.filltomatoes(p)
            f.close()
        return p

