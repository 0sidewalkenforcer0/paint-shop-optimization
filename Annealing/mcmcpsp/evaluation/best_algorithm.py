import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from typing import List
from ..solution import Solution
from ..solvers import COLOR_CHANGES_KEY
from .plotting_evaluation import PlottingEvaluation


ALGORITHM = 'Algorithm'
COLOR_CHANGES = 'Color changes'


class BestAlgorithm(PlottingEvaluation):
    def _prepare_plot(self, solutions: List[Solution]):
        data = pd.DataFrame(data=[
            [solution.algorithm,
             solution.gathered_data[COLOR_CHANGES_KEY]]
            for solution in solutions
        ], columns=[ALGORITHM, COLOR_CHANGES])
        min_val = data[COLOR_CHANGES].min()

        sns.set_theme(style='whitegrid')
        sns.boxplot(data=data, x=ALGORITHM, y=COLOR_CHANGES, hue=ALGORITHM, dodge=False).set(title=('Best solution: '+str(min_val)+' color changes'))
        plt.axhline(min_val)
        plt.legend()
