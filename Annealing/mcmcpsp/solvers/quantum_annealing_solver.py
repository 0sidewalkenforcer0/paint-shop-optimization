import logging
from .solver import Solver
from ..samplers import Sampler
from ..problem import Problem
from ..solution import Solution
from ..qubo import QuboCreation


class QuantumAnnealingSolver(Solver):
    def __init__(self, name, sampler: Sampler, qubo_creation: QuboCreation):
        self._sampler = sampler
        self._qubo_creation = qubo_creation
        self._name = name

    def solve(self, problem: Problem, **kwargs) -> Solution:
        logging.info(f"Solving problem using {self._name}")
        creator = self._qubo_creation.initialise(problem)
        qubo = creator.encode()
        solution = self._sampler.sample(qubo, **kwargs) if qubo else None
        result = creator.decode(solution)
        result.algorithm = self._name
        return result
