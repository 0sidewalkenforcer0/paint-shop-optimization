import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from typing import List
from ..solution import Solution
from .plotting_evaluation import PlottingEvaluation
from ..solvers import COLOR_CHANGES_KEY

ALGORITHM = 'Algorithm'
CAR_LINE = 'Carline Length'
IMPROVEMENT_OVER_RANDOM = 'Improvement over random'


class Lineplot(PlottingEvaluation):
    def _prepare_plot(self, solutions: List[Solution]):
        # divide solutions into algorithms lists
        list_random, solutions_all = ([] for i in range(2))
        for algo in solutions:
            if algo.algorithm=="random":
                list_random.append(algo)
       
        solutions_all = self.percentComparison(solutions, list_random)

        data = pd.DataFrame(data=[
            [solution[0].algorithm,
             len(solution[0].problem.carLine),
             solution[1]]
            for solution in solutions_all
        ], columns=[ALGORITHM, CAR_LINE, IMPROVEMENT_OVER_RANDOM])

        sns.lineplot(data=data, x=CAR_LINE, y=IMPROVEMENT_OVER_RANDOM, hue=ALGORITHM)
        plt.legend()


    # calculates the average of random algorithm from a carline length
    def getRandomAverage(self, car_line_length, list_random: List[Solution]):
        i, sum = (0 for i in range(2))
        if len(list_random) > 0:
            for elem in list_random:
                if len(elem.problem.carLine) == car_line_length:
                    sum += elem.gathered_data[COLOR_CHANGES_KEY]
                    i+=1
            return sum/i
        else:
            raise Exception("There are no random data to compare with")
    
    # calculates the percentage comparison from an algorithm to a random algorithm
    def percentComparison(self, list_algorithm: List[Solution], list_random: List[Solution]):
        list_percent = []
        for elem in list_algorithm:
            color_changes_random = self.getRandomAverage(len(elem.problem.carLine), list_random)
            color_changes_percent = 100*(1-((1+elem.gathered_data[COLOR_CHANGES_KEY])/(1+color_changes_random)))
            # list of tuples (Solution, color_changes_percent)
            list_percent.append((elem, color_changes_percent))

        return list_percent
