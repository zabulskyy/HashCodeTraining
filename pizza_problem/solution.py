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
                h, w = self.s[i][j]  # heigh and width of a slice
                if (h, w) != (0, 0):
                    if not self.p.isvalidslice(i, j, h, w):
                        return False
                    for xi in range(i, i + h + 1):
                        for xj in range(j, j + w + 1):
                            if occupied[xi][xj]:
                                return False
                            occupied[xi][xj] = True
        return True

    def out(self):
        pass

    def score(self):
        score = 0
        pizza_h, pizza_w = self.p.getheight(), self.p.getwidth()
        for i in range(pizza_h):  # coordinate i of a topleft cell of a slice
            for j in range(pizza_w):  # coordinate j of a topleft cell of a slice
                cell = self.s[i][j]
                if cell != (0, 0):
                    score += (cell[0] + 1) * (cell[1] + 1)
        return score


def test():
    instance = [
        [(1, 1), (0, 0), (2, 0)],
        [(0, 0), (0, 0), (0, 0)],
        [(0, 1), (0, 0), (0, 0)],
    ]
    s = Solution(Problem(), instance)
    print(s.is_ok())
    print(s.score())


class Problem:
    def getheight(self):
        return 3

    def getwidth(self):
        return 3

    def isvalidslice(self, i, j, h, w):
        return True


test()
