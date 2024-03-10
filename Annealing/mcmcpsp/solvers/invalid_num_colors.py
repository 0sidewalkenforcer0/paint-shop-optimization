import logging

from collections import defaultdict

from ..solution import Solution
from ..problem import Problem
from .tracking_solver import TrackingSolver


INVALID_NUM_COLORS_KEY ="invalid_num_colors"


class InvalidNumColors(TrackingSolver):
    def solve(self, problem: Problem, **kwargs) -> Solution:
        solution = self._internal.solve(problem, **kwargs)
        solution.gathered_data[INVALID_NUM_COLORS_KEY] =\
            InvalidNumColors.invalid_num_colors(solution)
        return solution

    @staticmethod
    def invalid_num_colors(solution: Solution) -> int:
        num_config_colors = defaultdict(int)
        #logging.debug('Calculate number of invalid colors')

        # Count how often each config color combination appears
        for position, color in enumerate(solution.assignments):
            config = solution.problem.carLine[position]
            num_config_colors[(config, color)] += 1

        num_invalid_colors = 0
        # Add deviation from expected value
        for (config, color), expected in solution.problem\
            .number_of_configuration_color_combinations\
            .items():

            value = num_config_colors.get((config, color))
            if value:
                num_config_colors.pop((config, color))
            else:
                value = 0
            num_invalid_colors += abs(expected - value)

        # Add invalid combinations
        for (config, color), value in num_config_colors.items():
            num_invalid_colors += value

        return num_invalid_colors
