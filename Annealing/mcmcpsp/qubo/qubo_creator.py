from abc import ABC, abstractmethod
from typing import Optional

from dimod import SampleSet, BinaryQuadraticModel

from ..problem import Problem
from ..solution import Solution


class QuboCreator(ABC):
    """Abstracts the generation of qubos and interpretation from a given
    problem.

    Single use object: It stores data during encoding and uses this data to
    decode the solution. Then it should be deleted.

    """
    def __init__(self, problem: Problem):
        self._problem = problem

    @abstractmethod
    def encode(self) -> Optional[BinaryQuadraticModel]:
        pass

    @abstractmethod
    def decode(self, sampleset: Optional[SampleSet]) -> Solution:
        pass


class QuboCreation(ABC):
    """Factory for `QuboCreator` used for configurating this single use item.

    """
    @abstractmethod
    def initialise(self, problem: Problem) -> QuboCreator:
        pass
