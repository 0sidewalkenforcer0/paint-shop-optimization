from time import time

from ..solution import Solution
from ..problem import Problem
from .tracking_solver import TrackingSolver

RUNTIME_KEY = "runtime"

class RuntimeTrackingSolver(TrackingSolver):
    def solve(self, problem: Problem, **kwargs) -> Solution:
        begin = time()
        solution = self._internal.solve(problem, **kwargs)
        end = time()
        solution.gathered_data[RUNTIME_KEY] = end - begin
        return solution
