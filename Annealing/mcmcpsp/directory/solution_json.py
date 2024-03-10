import json

from typing import TextIO

from ..solution import Solution
from .problem_json import problem_from_json_dict, problem_to_json_dict


PROBLEM_KEY = "problem"
ASSIGNMENTS_KEY = "assignments"
ALGORITHM_KEY = "algorithm"
GATHERED_DATA_KEY = "data"


def solution_to_json(solution: Solution, source: TextIO):
    return json.dump(solution_to_json_dict(solution), source)


def solution_to_json_dict(solution: Solution):
    return {
        PROBLEM_KEY: problem_to_json_dict(solution.problem),
        ASSIGNMENTS_KEY: solution.assignments,
        ALGORITHM_KEY: solution.algorithm,
        GATHERED_DATA_KEY: solution.gathered_data,
    }


def solution_from_json(source: TextIO) -> Solution:
    dictionary = json.load(source)
    return solution_from_json_dict(dictionary)


def solution_from_json_dict(dictionary) -> Solution:
    return Solution(
        problem=problem_from_json_dict(dictionary[PROBLEM_KEY]),
        assignments=dictionary[ASSIGNMENTS_KEY],
        algorithm=dictionary[ALGORITHM_KEY],
        gathered_data=dictionary[GATHERED_DATA_KEY],
    )
