class Solution:
    def __init__(self, Problem, solutionfield):
        """
        solutionfield: list 2x2 of (how_much_down, how_much_right) or (0, 0)
        """
        self.p = Problem
        self.s = solutionfield

    def is_ok(self):
        pizza_h, pizza_w = self.p.getheight(), self.p.getwidth()
        # (is_occupied, (coords of the owner))
        occupied = [[False] * pizza_w for _ in range(pizza_h)]
        for i in range(pizza_h):  # coordinate i of a topleft cell of a slice
            for j in range(pizza_w):  # coordinate j of a topleft cell of a slice
                # if self.s[i][j] == False :
                #    raise Exception("Cell ({} {}) isn't occupied".format(i, j))
                h, w = self.s[i][j]  # heigh and width of a slice
                if not self.p.isvalidslice(i, j, h, w):
                    raise Exception(
                        "Slice ({} {}), {} {} is not valid".format(i, j, h, w))
                for xi in range(i, i + h + 1):
                    for xj in range(j, j + w + 1):
                        print(xi, xj)
                        if occupied[xi][xj]:
                            raise Exception("Slice ({} {}), {} {} overlaps with cell ({} {})".format(
                                i, j, h, w, xi, xj))
                        if self.s[xi][xj] != (0, 0) and not (xi == i and xj == j):
                            raise Exception("Slice ({} {}), {} {} overlaps with cell ({} {})".format(
                                i, j, h, w, xi, xj))

            return True

    def out(self):
        pass

    def score(self):
        pass


def test():
    instance = [
        [(1, 1), (0, 0), (2, 0)],
        [(0, 0), (0, 0), (0, 0)],
        [(0, 2), (0, 0), (0, 0)],
    ]
    s = Solution(Problem(), instance)
    print(s.is_ok())


class Problem:
    def getheight(self):
        return 3

    def getwidth(self):
        return 3

    def isvalidslice(self, i, j, h, w):
        return True


test()
