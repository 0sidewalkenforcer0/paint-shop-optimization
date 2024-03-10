from abc import ABC, abstractmethod

from ..solution import Solution
from ..problem import Problem

class Solver(ABC):
    @abstractmethod
    def solve(self, problem: Problem, **kwargs) -> Solution:
        pass
