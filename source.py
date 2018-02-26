MAXN = 1000
MAXM = 1000

n, m = 0, 0
l, h = 0, 0

field = [[0] * MAXN for i in range(MAXN)]
solution = [[(0, 0)] * MAXN for i in range(MAXN)]

tomatoes = [[0] * MAXN for i in range(MAXN)]
mushrooms = [[0] * MAXN for i in range(MAXN)]


def valid(i, j):
    return i >= 0 and i < n and j >= 0 and j < m


def filltomatoes():
    global field, tomatoes
    tomatoes[0][0] = 1 if field[0][0] == 'T' else 0
    for i in range(1, n):
        tomatoes[i][0] = 1 if field[i][0] == 'T' else 0
        tomatoes[i][0] += tomatoes[i - 1][0]
    for j in range(1, m):
        tomatoes[0][j] = 1 if field[0][j] == 'T' else 0
        tomatoes[0][j] += tomatoes[0][j - 1]
    for i in range(1, n):
        for j in range(1, m):
            tomatoes[i][j] = 1 if field[i][j] == 'T' else 0
            tomatoes[i][j] += (tomatoes[i - 1][j] + tomatoes[i][j - 1] - tomatoes[i - 1][j - 1])


def fillmushrooms():
    global field, mushrooms
    mushrooms[0][0] = 1 if field[0][0] == 'M' else 0
    for i in range(1, n):
        mushrooms[i][0] = 1 if field[i][0] == 'M' else 0
        mushrooms[i][0] += mushrooms[i - 1][0]
    for j in range(1, m):
        mushrooms[0][j] = 1 if field[0][j] == 'M' else 0
        mushrooms[0][j] += mushrooms[0][j - 1]
    for i in range(1, n):
        for j in range(1, m):
            mushrooms[i][j] = 1 if field[i][j] == 'M' else 0
            mushrooms[i][j] += (mushrooms[i - 1][j] + mushrooms[i][j - 1] - mushrooms[i - 1][j - 1])


def gettomatos(uplefti, upleftj, height, width):
    global tomatoes
    i = uplefti + height - 1
    j = upleftj + width - 1
    result = tomatoes[i][j]
    if (valid(uplefti - 1, j)): result -= tomatoes[uplefti - 1][j]
    if (valid(i, upleftj - 1)): result -= tomatoes[i][upleftj - 1]
    if (valid(uplefti - 1, upleftj - 1)): result += tomatoes[uplefti - 1][upleftj - 1]
    return result


def getmushrooms(uplefti, upleftj, height, width):
    global mushrooms
    i = uplefti + height - 1
    j = upleftj + width - 1
    result = mushrooms[i][j]
    if (valid(uplefti - 1, j)): result -= mushrooms[uplefti - 1][j]
    if (valid(i, upleftj - 1)): result -= mushrooms[i][upleftj - 1]
    if (valid(uplefti - 1, upleftj - 1)): result += mushrooms[uplefti - 1][upleftj - 1]
    return result


def score(solution):
    pass


def evaluatesolution(solution):
    # is ok or not
    occupied = [[False] * MAXN for i in range(MAXN)]


def outsolutions(solution):
    pass


def read():
    global n, m, l, h, field
    n, m, l, h = map(int, input().split())
    for i in range(n):
        row = input()
        for j in range(m):
            field[i][j] = row[j]


read()
fillmushrooms()
filltomatoes()
