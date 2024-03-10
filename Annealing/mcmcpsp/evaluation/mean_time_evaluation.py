from .evaluation import Evaluation
from typing import List
from ..solvers.runtime_tracking_solver import RUNTIME_KEY


class MeanTimeEvaluation(Evaluation):
    def evaluate(self, solution: List):
        sum_of_time = 0
        for i in range(len(solution)):
            sum_of_time += solution[i].gathered_data[RUNTIME_KEY]
        mean_time = sum_of_time / len(solution)
        print("The mean of time:", mean_time)
