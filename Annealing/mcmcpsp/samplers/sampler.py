from abc import ABC, abstractmethod

from dimod import BinaryQuadraticModel, SampleSet

class Sampler(ABC):
    @abstractmethod
    def sample(self, problem: BinaryQuadraticModel, **kwargs) -> SampleSet:
        pass
