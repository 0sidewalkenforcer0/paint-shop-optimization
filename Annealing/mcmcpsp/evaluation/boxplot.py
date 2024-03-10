from typing import List

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from ..solution import Solution
from .plotting_evaluation import PlottingEvaluation
from ..solvers import COLOR_CHANGES_KEY

ALGORITHM = 'Algorithm'
CAR_LINE = 'Carline Length'
COLOR_CHANGES = 'Color changes'


class Boxplot(PlottingEvaluation):
    def _prepare_plot(self, solutions: List[Solution]):
        data = pd.DataFrame(data=[
            [solution.algorithm,
             len(solution.problem.carLine),
             solution.gathered_data[COLOR_CHANGES_KEY]]
            for solution in solutions
        ], columns=[ALGORITHM, CAR_LINE, COLOR_CHANGES])


        sns.boxplot(data=data, x=CAR_LINE, y=COLOR_CHANGES, hue=ALGORITHM)
        plt.legend()
