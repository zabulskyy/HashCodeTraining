MAXN = 1000
MAXM = 1000

n, m = 0,0
l, h = 0,0

field = [[0] * MAXN for i in range(MAXN)]
solution = [[(0, 0)] * MAXN for i in range(MAXN)]

tomatoes = [[0] * MAXN for i in range(MAXN)]
mushrooms = [[0] * MAXN for i in range(MAXN)]

def valid(i, j):
    return i >= 0 and i < n and j >= 0 and j < m
def filltomatoes():
    global field
    tomatoes[0][0] = 1 if field


def gettomatos(uplefti, upleftj, height, width):
    pass
def getmushrooms(uplefti, upleftj, height, width):
    pass

def score(solution):
    pass
def outsolutions(solution):
    pass

def read():
    global n, m, l, h, field
    n, m, l, h = map(int, input().split())
    for i in range(n):
        row = input()
        for j in range(m):
            field[i][j] = row[j]