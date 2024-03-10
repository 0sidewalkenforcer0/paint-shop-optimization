from abc import ABC, abstractmethod
from typing import List


class Evaluation(ABC):
    @abstractmethod
    def evaluate(self, solution: List):
        pass
