from dataclasses import dataclass, field
import logging
from typing import Any, Dict

import dwave.system as ds
from dimod import BinaryQuadraticModel, SampleSet
from uqo.client.config import Config
from uqo.Problem import Qubo
from minorminer import find_embedding

from .sampler import Sampler

NUM_SAMPLES = 50

@dataclass
class UQOSampler(Sampler):
    config: Config
    platform: str
    solver: str
    num_samples: int

    def sample(self, problem: BinaryQuadraticModel, **kwargs) -> SampleSet:
        relabeled_problem, mapping = problem.relabel_variables_as_integers(inplace=False)

        qubo, offset = relabeled_problem.to_qubo()
        qubo = Qubo(self.config, qubo)\
            .with_platform(self.platform)\
            .with_solver(self.solver)

        result = self._prepare_qubo(qubo, relabeled_problem, **kwargs)\
                     .solve(self.num_samples).sampleset

        result.relabel_variables(mapping, inplace=True)
        result.record.energy += offset
        return result

    def _prepare_qubo(self, qubo: Qubo, problem: BinaryQuadraticModel, **kwargs):
        return qubo


@dataclass
class FujitsuSampler(UQOSampler):
    platform: str = 'fujitsu'
    solver: str = 'DAU'
    num_samples: int = NUM_SAMPLES

    def _prepare_qubo(self, qubo: Qubo, problem: BinaryQuadraticModel, **kwargs):
        return qubo\
            .with_params(
                optimization_method="annealing",
            )


@dataclass
class DWaveSampler(UQOSampler):
    lock: Any = None
    cached_embedding: Any = None
    platform: str = 'dwave'
    solver: str = 'Advantage_system4.1'
    num_samples: int = NUM_SAMPLES

    def _prepare_qubo(self, qubo: Qubo, problem: BinaryQuadraticModel, name: str):
        with self.lock:
            embedding = self.cached_embedding.get(name)
            if embedding:
                qubo.embedding = embedding
            else:
                logging.info(f"Embedding QUBO for {name}!")
                reference = ds.DWaveSampler(solver=self.solver).edgelist
                embedding = find_embedding(problem.quadratic, reference)
                self.cached_embedding[name] = embedding
                qubo.embedding = embedding

        return qubo
