import matplotlib.pyplot as plt
import tikzplotlib

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from pathlib import Path

from .evaluation import Evaluation

@dataclass
class PlottingEvaluation(Evaluation, ABC):
    filename: Path

    def evaluate(self, solution: List):
        # sorting algorithm alphabetically
        for _ in solution:
            solution.sort(key = lambda l: l.algorithm)
        
        self._prepare_plot(solution)

        if self.filename.suffix == ".tex":
            tikzplotlib.save(self.filename)
        else:
            plt.savefig(self.filename)


    @abstractmethod
    def _prepare_plot(self, solution: List):
        pass
