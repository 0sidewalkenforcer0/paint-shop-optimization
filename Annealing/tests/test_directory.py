from io import StringIO
from pathlib import Path
from typing import List, Tuple, Set
from tempfile import TemporaryDirectory
from string import ascii_letters

from hypothesis import given
from hypothesis.strategies import text, composite, sets


from mcmcpsp.problem import Problem
from mcmcpsp.solution import Solution
from mcmcpsp.solvers import RandomSolver
from mcmcpsp.directory import problem_to_json, problem_from_json, \
    solution_to_json, solution_from_json, Directory

from .test_integration import integer_problem_instance, integer_solution


MAX_NAME_LENGTH = 10
MAX_PROBLEMS = 100
MAX_SOLUTIONS = 100


@composite
def name(draw, max_name_length: int = MAX_NAME_LENGTH):
    return draw(text(ascii_letters, min_size=1, max_size=max_name_length))


@composite
def name_set(draw, max_count: int, name = name()) -> Set[str]:
    return draw(sets(name, min_size=1, max_size=max_count))


@composite
def named_problems(draw,
                   name,
                   problem,
                   max_problems: int = MAX_PROBLEMS,
                   ) -> List[Tuple[str, Problem[int, int]]]:
    names = draw(name_set(max_problems, name))
    return [
        (name, draw(problem))
        for name in names
    ]


@composite
def named_solutions(draw,
                   name,
                   solution,
                   max_solutions: int = MAX_SOLUTIONS,
                   ) -> List[Tuple[str, Solution[int, int]]]:
    names = draw(name_set(max_solutions, name))
    return [
        (name, draw(solution))
        for name in names
    ]


@given(integer_problem_instance())
def test_problem_serialisation_is_inverse(problem: Problem[int, int]):
    string = StringIO()
    problem_to_json(problem, string)
    string.seek(0)
    decoded_problem = problem_from_json(string)
    assert problem == decoded_problem


@given(integer_problem_instance())
def test_solution_serialisation_is_inverse(problem: Problem[int, int]):
    solution = RandomSolver().solve(problem)

    string = StringIO()
    solution_to_json(solution, string)
    string.seek(0)
    decoded_solution = solution_from_json(string)
    assert solution == decoded_solution


@given(named_problems(name(), integer_problem_instance()))
def test_problem_storing_is_inverse(problems: List[Tuple[str, Problem[int, int]]]):
    with TemporaryDirectory() as file:
       directory = Directory(Path(file))

       directory.storeProblems(problems)
       loaded_problems = list(directory.fetchProblems())

       for problem in problems:
           assert problem in loaded_problems

       for problem in loaded_problems:
           assert problem in problems


@given(named_solutions(name(), integer_solution()))
def test_solution_storing_is_inverse(solutions: List[Tuple[str, Solution[int, int]]]):
    with TemporaryDirectory() as file:
       directory = Directory(Path(file))

       directory.storeSolutions(solutions)
       loaded_solutions = list(directory.fetchSolutions())

       for solution in solutions:
           assert solution in loaded_solutions

       for solution in loaded_solutions:
           assert solution in solutions
