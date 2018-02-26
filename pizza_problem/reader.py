from problem import *
class Reader:
    def __init__(self):
        pass

    def read(self):
        n, m, t, h = [int(x) for x in input().split()]
        f = []
        for i in range(n):
            l = input()
            f.append(list(l))
        return Problem(f, t, h)