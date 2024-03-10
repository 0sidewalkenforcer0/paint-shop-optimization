import logging
from pathlib import Path
from typing import Tuple, Iterable

from ..problem import Problem
from ..solution import Solution

from .problem_json import problem_from_json, problem_to_json
from .solution_json import solution_from_json, solution_to_json


PROBLEM_FILE_EXTENSION = ".json"
SOLUTION_FILE_EXTENSION = ".json"
PROBLEM_NAME_KEY = "problem"


class AlreadyExistingFileException(Exception):
    def __init__(self, existing_file: str):
        self.existing_file = existing_file


class Directory:
    """Encapsulates how problems and solutions are store persistently.

    """
    _PROBLEM_DIRECTORY = "problems"
    _SOLUTION_DIRECTORY = "solutions"
    _PER_PROBLEM_DIRECTORY = "solutions_per_problem"
    _PER_ALGORITHM_DIRECTORY = "solutions_per_algorithm"

    def __init__(self, directory: Path):
        self._directory = directory
        self._problem_directory  = self._directory / self._PROBLEM_DIRECTORY
        self._problem_directory.mkdir(parents=True, exist_ok=True)

        self._solution_directory  = self._directory / self._SOLUTION_DIRECTORY
        self._solution_directory.mkdir(parents=True, exist_ok=True)

        self._per_problem_directory  = self._solution_directory / self._PER_PROBLEM_DIRECTORY
        self._per_problem_directory.mkdir(parents=True, exist_ok=True)

        self._per_algorithm_directory  = self._solution_directory / self._PER_ALGORITHM_DIRECTORY
        self._per_algorithm_directory.mkdir(parents=True, exist_ok=True)

    def fetchProblems(self) -> Iterable[Tuple[str, Problem]]:
        """Enumerates all problems the directory contains.

        """

        logging.info('fetch problems from directory')
        for problem in self._problem_directory\
                   .glob(f"*{PROBLEM_FILE_EXTENSION}"):
            with problem.open('r') as file:
                yield problem.stem, problem_from_json(file)

    def fetchProblemNames(self) -> Iterable[str]:
        """Enumerates all problem names the directory contains.

        """
        logging.info('fetch problem names from directory')
        # Find all json-files in the problem directory.
        return (str(problem_file.stem)
                for problem_file in self._problem_directory\
                   .glob(f"*{PROBLEM_FILE_EXTENSION}"))

    def storeProblems(self, problems: Iterable[Tuple[str, Problem]], replace: bool=False):
        """Stores `problems` with the given name inside the directory.

        """
        for i, (name, problem) in enumerate(problems):
            filename = self._problem_directory / (name + PROBLEM_FILE_EXTENSION)
            logging.info('store problem ' + name + ' (' + str(i+1) + ' of ' + str(len(problems)) +  ') to directory')
            if filename.exists() and not replace:
                raise AlreadyExistingFileException(name)
            else:
                with filename.open('w') as file:
                    problem_to_json(problem, file)

    def fetchSolutions(self) -> Iterable[Tuple[str, Solution]]:
        """Enumerates all solutions the directory contains.

        """
        logging.info('fetch solutions from directory')
        for solution in self._solution_directory\
                   .glob(f"*{SOLUTION_FILE_EXTENSION}"):
            with solution.open('r') as file:
                yield solution.stem, solution_from_json(file)

    def fetchSolutionNames(self) -> Iterable[str]:
        """Enumerates all solution names the directory contains.

        """
        logging.info('fetch solution names from directory')
        # Find all json-files in the solution directory.
        return (str(solution_file.stem)
                for solution_file in self._solution_directory\
                   .glob(f"*{SOLUTION_FILE_EXTENSION}"))

    def storeSolutions(self, solutions: Iterable[Tuple[str, Solution]], replace: bool=False):
        """Stores `solutions` with the given name inside the directory.

        """
        logging.info('store solution ' + solutions[0][0] + ' to directory')
        for name, solution in solutions:
            filename = name + SOLUTION_FILE_EXTENSION
            solution_file = self._solution_directory/filename
            if solution_file.exists() and not replace:
                raise AlreadyExistingFileException(name)

            # Store solution in main directory
            with solution_file.open('w') as file:
                solution_to_json(solution, file)

            # Store solution inside the corresponding algorithm directory
            per_algorithm = self._per_algorithm_directory/solution.algorithm
            per_algorithm.mkdir(parents=True, exist_ok=True)
            solution_file.link_to(per_algorithm/filename)

            # Store solution inside the corresponding problem directory
            per_problem = self._per_problem_directory/solution.gathered_data[PROBLEM_NAME_KEY]
            per_problem.mkdir(parents=True, exist_ok=True)
            solution_file.link_to(per_problem/filename)

