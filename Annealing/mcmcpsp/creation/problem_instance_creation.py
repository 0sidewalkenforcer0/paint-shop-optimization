from abc import ABC, abstractmethod
from typing import Generic
from ..problem import Problem, Color, Config


class ProblemInstanceCreation(Generic[Color, Config], ABC):
    """Creates instances of the paint shop problem with arbitrary color and
    configuration types

    """
    @abstractmethod
    def createInstance(self) -> Problem[Color, Config]:
        pass
