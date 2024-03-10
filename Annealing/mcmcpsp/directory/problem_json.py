import json

from typing import TextIO

from ..problem import Problem


COLORS_KEY = "colors"
CONFIGS_KEY = "configs"
CARLINE_KEY = "carline"
NUM_OCCURRENCES_KEY = "num_occurrences"


def problem_to_json(problem: Problem, source: TextIO):
    return json.dump(problem_to_json_dict(problem), source)


def problem_to_json_dict(problem: Problem):
    return {
        COLORS_KEY: list(problem.colors),
        CONFIGS_KEY: list(problem.configurations),
        CARLINE_KEY: problem.carLine,
        NUM_OCCURRENCES_KEY: [
            [config, color, num_occurrences]
            for (config, color), num_occurrences
            in problem.number_of_configuration_color_combinations.items()
        ]
    }


def problem_from_json(source: TextIO) -> Problem:
    dictionary = json.load(source)
    return problem_from_json_dict(dictionary)


def problem_from_json_dict(dictionary) -> Problem:
    return Problem(
        colors=set(dictionary[COLORS_KEY]),
        configurations=set(dictionary[CONFIGS_KEY]),
        carLine=dictionary[CARLINE_KEY],
        number_of_configuration_color_combinations=\
            {(config, color): num_occurrences
             for (config, color, num_occurrences)
             in dictionary[NUM_OCCURRENCES_KEY]
             }
    )
