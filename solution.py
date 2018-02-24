from problem import Problem
from copy import deepcopy

import random
import hashlib

class Solution:
    p = None
    slices = None
    free = None
    slice_list = None

    def __init__(self, problem):
        self.p = problem    # type: Problem
        self.slices = [[(0, 0)] * self.p.max_width for i in range(self.p.max_height)]
        self.free = [[True] * self.p.max_width for i in range(self.p.max_height)]
        self.slice_list = []

    def score(self):
        score = 0
        for i in range(self.p.max_height):
            score += self.p.max_width - self.free[i].count(True)
        return score

    def is_OK(self):
        for i in range(self.p.max_height):
            for j in range(self.p.max_width):
                if self.slices[i][j] != (0, 0):
                    h, w = self.slices[i][j]
                    if not self.p.valid(i+h-1, j+w-1):
                        return False, "Slice {},{} outbounds pizza size by {},{}".format(i, j, h, w)
                    if h*w > self.p.H:
                        return False, "Slice {},{},{},{} outsizes maximum size {}".format(i, j, h, w, self.p.H)
                    ts, ms = 0, 0
                    for xi in range(i, i+h):
                        for xj in range(j, j+h):
                            if self.slices[xi][xj] != (0, 0):
                                return False, "Slice {},{},{},{} overlaps with slice {},{},{},{}".format(i, j, h, w, xi, xj, self.slices[xi][xj][0], self.slices[xi][xj][1])
                            if self.p.field[xi][xj] == 'T':
                                ts += 1
                            if self.p.field[xi][xj] == 'M':
                                ms += 1
                    if ts<self.p.L:
                        return False, "Slice {},{},{},{} has not enough tomatos: {}, but need to be {}".format(i, j, h, w, ts, self.p.L)
                    if ms<self.p.L:
                        return False, "Slice {},{},{},{} has not enough mushrooms: {}, but need to be {}".format(i, j, h, w, ms, self.p.L)
        return True, "Solution is valid!"

    def print_free(self):
        print("\n".join(["".join(['_' if self.free[i][j]==True else 'X' for j in range(self.p.max_width)]) for i in
                         range(self.p.max_height)]))

    def _prepare_string(self):
        self.get_all_slices()
        table = [['_'] * self.p.max_width for i in range(self.p.max_height)]
        alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        alphabet_n = len(alphabet)
        k = 0
        for slice in self.slice_list:
            for i in range(slice[0], slice[0] + slice[2]):
                for j in range(slice[1], slice[1] + slice[3]):
                    table[i][j] = alphabet[k]
            k += 1
            k = k % alphabet_n
        return table

    def print_solution(self):
        table = self._prepare_string()
        print("\n".join(["".join([table[i][j] for j in range(self.p.max_width)]) for i in range(self.p.max_height)]))

    def out(self):
        pass

    def get_hash(self, is_string=False):
        m = hashlib.md5()
        table = self._prepare_string()
        m.update("".join(["".join([table[i][j] for j in range(self.p.max_width)]) for i in range(self.p.max_height)]))
        if is_string:
            return m.hexdigest()
        return m.digest()

    def is_free_space(self, upperi, upperj, height, width):
        if not self.p.valid(upperi+height-1, upperj+width-1):
            return False
        for i in range(upperi, upperi+height):
            for j in range(upperj, upperj+width):
                if self.free[i][j] != True:
                    return False
        return True

    def create_new_slice(self, upperi, upperj, height, width):
        if not self.p.valid(upperi+height-1, upperj+width-1):
            return
        self.slices[upperi][upperj] = (height, width)
        for i in range(upperi, upperi+height):
            for j in range(upperj, upperj+width):
                # self.free[i][j] = False
                self.free[i][j] = (upperi, upperj)

    def get_all_slices(self):
        self.slice_list = []
        for i in range(self.p.max_height):
            for j in range(self.p.max_width):
                if self.slices[i][j] != (0, 0):
                    self.slice_list.append((i,j) + self.slices[i][j])
        return self.slice_list

    def pick_random_slice(self):
        if not self.slice_list:
            self.get_all_slices()
        return self.slice_list[random.randint(0,len(self.slice_list)-1)]

    def duplicate(self):
        s = Solution(self.p)
        s.slices = deepcopy(self.slices)
        s.slice_list = deepcopy(self.slice_list)
        s.free = deepcopy(self.free)
        return s

    def get_overlaps(self, upperi, upperj, height, width):
        overlapped_slices = set()
        overlapped_pices = []
        for i in range(upperi, upperi + height):
            if i>=self.p.max_height:
                break
            for j in range(upperj, upperj + width):
                if j>=self.p.max_width:
                    break
                if self.free[i][j] != True:
                    overlapped_pices += [(i,j)]
                    overlapped_slices.add(self.free[i][j])
        return overlapped_slices, overlapped_pices

    def delete_slice(self, upperi, upperj):
        h, w = self.slices[upperi][upperj]
        if (h, w) == (0, 0):
            return
        for i in range(upperi, upperi + h):
            for j in range(upperj, upperj + w):
                self.free[i][j] = True
        self.slices[upperi][upperj] = (0, 0)

