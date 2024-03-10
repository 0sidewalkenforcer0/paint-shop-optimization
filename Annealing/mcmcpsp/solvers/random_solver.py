import random
import logging

from collections import defaultdict

from ..solution import Solution
from ..problem import Problem
from .solver import Solver

SOLVER_NAME = "random"

class RandomSolver(Solver):
    """Randomly creates color assignments.

    """
    def solve(self, problem: Problem, **kwargs) -> Solution:
        # Create for each configuration a list of colors
        # holding the number constraints.

        logging.info('solving problem using random algorithm')

        color_assignments = defaultdict(list)
        for (config, color), num_occurrences in problem.number_of_configuration_color_combinations.items():
            color_assignments[config].extend([color] * num_occurrences)

        # Reorder colors for each configuration randomly
        for colors in color_assignments.values():
            random.shuffle(colors)

        # Go through the car line and for the respective configuration choose
        # colors in the order randomly created above.
        color_car_line = []
        for config in problem.carLine:
            color = color_assignments[config].pop()
            color_car_line.append(color)

        return Solution(
            problem,
            color_car_line,
            SOLVER_NAME,
            dict()
        )
