import logging
from ..solution import Solution
from ..problem import Problem
from .solver import Solver


SOLVER_NAME = "greedy"


class GreedySolver(Solver):
    """Uses greedy algorithm for color assignments.

    """
    def solve(self, problem: Problem, **kwargs) -> Solution:
        logging.info('solving problem using greedy algorithm')

        # define variables
        curr_color = None
        # empty list of color assignments to carLine
        color_car_line = []
        # dictionary with the number of occurences for each config color combination
        dictionary = problem.number_of_configuration_color_combinations.copy()

        # iterate through carLine
        for config in problem.carLine:
            # check if config color combination is NOT in dictionary
            if (config, curr_color) not in dictionary:
                # get next available color for this configuration
                curr_color = next(key for key in dictionary.keys() if key[0] == config)[1]

            # get the number of occurences for this config color combination
            occurrences = dictionary[(config, curr_color)]

            # append current color to color_car_line
            color_car_line.append(curr_color)

            # number of ocurrences is greater than 1 -> decrease occurrences for this key by 1
            if occurrences > 1:
                dictionary[(config, curr_color)] = occurrences - 1
            # last available config color combination was used -> pop key from dictionary
            else:
                dictionary.pop((config, curr_color))


        return Solution(
            problem,
            color_car_line,
            SOLVER_NAME,
            dict()
            )
       
