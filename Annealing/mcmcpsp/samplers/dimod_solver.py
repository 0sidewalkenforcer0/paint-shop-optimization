import neal
import dimod

from dataclasses import dataclass

from dimod import BinaryQuadraticModel, SampleSet
from dwave_qbsolv import QBSolv

from .sampler import Sampler


@dataclass
class DimodSampler(Sampler):
    sampler: dimod.Sampler

    def sample(self, problem: BinaryQuadraticModel, **kwargs) -> SampleSet:
        return self.sampler.sample(problem)


class QBSolvSampler(DimodSampler):
    def __init__(self):
        super().__init__(QBSolv())


class SimulatedAnnealingSampler(DimodSampler):
    def __init__(self):
        super().__init__(neal.SimulatedAnnealingSampler())
