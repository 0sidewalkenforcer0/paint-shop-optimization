from .evaluation import Evaluation
from typing import List
from ..solvers.color_change_tracking_solver import COLOR_CHANGES_KEY


class ColorChangesEvaluation(Evaluation):
    def evaluate(self, solution: List):
        num_of_color_change = 0
        for i in range(len(solution)):
            num_of_color_change += solution[i].gathered_data[COLOR_CHANGES_KEY]
        average_color_changes = num_of_color_change / len(solution)
        print("The mean times of color changes:", average_color_changes)
