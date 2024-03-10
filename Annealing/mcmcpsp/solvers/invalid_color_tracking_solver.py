import logging
from ..solution import Solution
from ..problem import Problem
from .tracking_solver import TrackingSolver


INVALID_COLORS_KEY ="invalid_colors"


class InvalidColorTrackingSolver(TrackingSolver):
    def solve(self, problem: Problem, **kwargs) -> Solution:
        solution = self._internal.solve(problem, **kwargs)
        solution.gathered_data[INVALID_COLORS_KEY] =\
            InvalidColorTrackingSolver.invalid_colors(solution)
        return solution

    @staticmethod
    def invalid_colors(solution: Solution) -> int:
        num_invalid_colors = 0
        logging.debug('Calculate number of invalid colors')
        for position, color in enumerate(solution.assignments):
            if color not in solution.problem.colors_of_car_line[position]:
                num_invalid_colors += 1
        return num_invalid_colors
