from ..problem import Problem
from .qubo_creator import QuboCreation
from .simple_qubo import SimpleQuboCreator


class AdaptiveWeightsQuboCreation(QuboCreation):
    def initialise(self, problem: Problem) -> SimpleQuboCreator:
        bound = len(problem.colors) * len(problem.carLine)
        return SimpleQuboCreator(
            problem,
            bound,
            bound,
            1,
            2,
        )
