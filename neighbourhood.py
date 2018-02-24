from problem import Problem
from solution import Solution

import random

class Neighbourhood:

    s = None
    p = None

    def __init__(self, problem):
        self.p = problem    # type: Problem

    def get_neighbours(self, solution):
        return []

    def fill_gaps(self, solution, region):
        """
        :param solution:
         @:type Solution
        :param region: [upperi, upperj, lower_right_i, lower_right_j]
        """
        formats = self.p.slices_formats()
        random.shuffle(formats)
        for r in region:
            for f in formats:
                if solution.is_free_space(r[0], r[1], f[0], f[1]) and self.p.is_valid_slice(r[0], r[1], f[0], f[1]):
                    solution.create_new_slice(r[0], r[1], f[0], f[1])

class Neighbourhood_ChangeFormats(Neighbourhood):
    ###
    # Pick random slice
    # Change format of the slice
    # Fill the gaps
    ###
    def get_neighbours(self, solution):
        """
        :param solution:
         @:type Solution
        :rtype: list[Solution]
        """
        result = []

        formats = self.p.slices_formats()
        si, sj, sh, sw = solution.pick_random_slice()

        for f in formats:
            if f[0]==sh and f[1]==sw:
                continue
            if not self.p.is_valid_slice(si, sj, f[0], f[1]):
                continue
            new_sol = solution.duplicate()      # type: Solution

            # delete all overlapped slices
            overlaps, region = new_sol.get_overlaps(si, sj, f[0], f[1])
            for slice in overlaps:
                new_sol.delete_slice(slice[0], slice[1])

            # print("After deletion")
            # new_sol.print_solution()
            # new_sol.print_free()

            # create a slice with new format and fill gaps
            new_sol.create_new_slice(si, sj, f[0], f[1])
            self.fill_gaps(new_sol, region)

            # print("After filling gaps")
            # new_sol.print_solution()
            # new_sol.print_free()

            if new_sol.is_OK():
                result.append(new_sol)

        return result

class Neighbourhood_FillGaps(Neighbourhood):
    ###
    # Pick random slice(s)
    # Delete slice(s)
    # Fill the gaps
    ###

    def __init__(self):
        self.slice_2_delete = 1

    def get_neighbours(self, solution):
        """
        :param solution:
         @:type Solution
        :rtype: list[Solution]
        """
        result = []

        formats = self.p.slices_formats()
        slices = [solution.pick_random_slice() for i in range(self.slice_2_delete)]

        new_sol = solution.duplicate()
        for slice in slices:
            new_sol.delete_slice(slice[0], slice[1])




