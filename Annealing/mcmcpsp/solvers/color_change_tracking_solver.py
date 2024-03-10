import logging
from ..solution import Solution
from ..problem import Problem
from .tracking_solver import TrackingSolver


COLOR_CHANGES_KEY ="color_changes"


class ColorChangeTrackingSolver(TrackingSolver):
    def solve(self, problem: Problem, **kwargs) -> Solution:
        solution = self._internal.solve(problem, **kwargs)
        solution.gathered_data[COLOR_CHANGES_KEY] = ColorChangeTrackingSolver\
                .numberOfColorChanges(solution)
        return solution

    @staticmethod
    def numberOfColorChanges(solution: Solution) -> int:
        num_changes = 0
        logging.debug('calculate numerOfColorChanges')
        for i in range(len(solution.assignments)-1):
            # Check if directly succeeding colors are equal.
            if solution.assignments[i] != solution.assignments[i+1]:
                num_changes += 1
        return num_changes
