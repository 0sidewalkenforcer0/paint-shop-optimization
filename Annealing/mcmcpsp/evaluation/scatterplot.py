from typing import List

import pandas as pd
import seaborn as sns

from ..solution import Solution
from .plotting_evaluation import PlottingEvaluation
from ..solvers import COLOR_CHANGES_KEY
from ..qubo import ENERGY_KEY

ALGORITHM = 'Algorithm'
CAR_LINE = 'Carline Length'
COLOR_CHANGES = 'Color changes'
ENERGY = 'energy'


class Scatterplot(PlottingEvaluation):
    def _prepare_plot(self, solutions: List[Solution]):
        data = pd.DataFrame(data=[
            [
                solution.gathered_data[COLOR_CHANGES_KEY],
                solution.gathered_data[ENERGY_KEY]
            ]
            for solution in solutions
            if solution.gathered_data.get(ENERGY_KEY)
        ], columns=[COLOR_CHANGES, ENERGY])
        sns.scatterplot(data=data, x=COLOR_CHANGES, y=ENERGY)

