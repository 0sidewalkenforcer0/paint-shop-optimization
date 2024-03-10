from collections import defaultdict
from dataclasses import dataclass
from typing import Optional


from dimod import SampleSet, BinaryQuadraticModel
from pyqubo import Binary, Base, Constraint

from ..problem import Problem
from ..solution import Solution
from .qubo_creator import QuboCreator, QuboCreation


SIMPLE_QUBO_NAME = "simple_qubo"
ENERGY_KEY = "energy"
NUM_QUBITS_KEY = "num_qubits"


class SimpleQuboCreator(QuboCreator):
    """QUBO used in the submission

    """
    def __init__(self, problem: Problem,
                 exactly_one_color_weight: float,
                 exactly_num_config_color_weight: float,
                 minimal_color_changes_weight: float,
                 single_color_config_weight: float,
                 ):
        super().__init__(problem)

        self._singletons, non_singletons = self.identifySingletons(problem.colors_of_car_line)

        #
        positions_of_color_config = self.positions_of_config_color(
            non_singletons,
            problem.carLine
        )

        self._position_color = {
            (position, color): Binary(self.variable_name(position, color))
            for position, colors in non_singletons.items()
            for color in colors
        }

        variables_of_config_color = {
            (config, color): {
                self._position_color[(position, color)]
                for position in positions
            }
            for (config, color), positions in positions_of_color_config.items()
        }


        constraints = {
            "exactly_one_color": (
                exactly_one_color_weight,
                self._exactly_one_color(non_singletons)
            ),
            "exactly_num_config_color": (
                exactly_num_config_color_weight,
                self._exactly_num_config_color(variables_of_config_color),
            ),
            "minimal_color_change": (
                minimal_color_changes_weight,
                self._minimal_color_change(non_singletons),
            ),
            "single_color_config": (
                single_color_config_weight,
                self._single_color_config(self._singletons),
            )
        }

        model = sum(
            weight * Constraint(constraint, label=name)
            for name, (weight, constraint) in constraints.items()
            if isinstance(constraint, Base)
        )

        if isinstance(model, Base):
            self._qubo = model.compile().to_bqm()
        else:
            self._qubo = None

    def identifySingletons(self, colors_of_carline):
        """Splits all positions

        """
        singletons = dict()
        non_singletons = dict()

        for position, colors in enumerate(colors_of_carline):
            if len(colors) == 1:
                singletons[position] = list(colors)[0]
            else:
                non_singletons[position] = colors

        return singletons, non_singletons

    def positions_of_config_color(self, non_singletons, carline):
        result = defaultdict(set)

        for position, colors in non_singletons.items():
            config = carline[position]
            for color in colors:
                result[(config, color)].add(position)

        return dict(result)

    def encode(self) -> Optional[BinaryQuadraticModel]:
        return self._qubo

    @staticmethod
    def variable_name(position: int, color) -> str:
        return f"{position}_{color}"

    def decode(self, sampleset: Optional[SampleSet]) -> Solution:
        assignments = [None] * len(self._problem.carLine)

        # Check if sampleset is empty
        if  sampleset:
            # Choose best solution
            best = sampleset.first

            # Check if color bit is active
            for position, color in self._position_color:
                variable = self.variable_name(position, color)
                value = int(best.sample[variable])
                if value == 1:
                    assignments[position] = color
            energy = best.energy
            num_qubits = len(best.sample)
        # For any empty set no variables have been used.
        else:
            energy = 0.0
            num_qubits = 0

        # Restore colors of isolated configurations
        for position, color in self._singletons.items():
            assignments[position] = color

        return Solution(
            self._problem,
            assignments,
            algorithm=SIMPLE_QUBO_NAME,
            gathered_data={
                ENERGY_KEY: energy,
                NUM_QUBITS_KEY: num_qubits,
            }
        )

    def _color_occurrences(self, position, non_singleton):
        """Counts how many colors are set at the specified position.

        """
        return sum(
            self._position_color[(position, color)]
            for color in non_singleton[position]
        )

    def _exactly_one_color(self, non_singletons):
        """A constraint that is zero iff for each position exactly one color is
        chosen. Any other case is penalised.

        """
        return sum(
            (self._color_occurrences(position, non_singletons) - 1)**2
            for position in non_singletons
         )

    def _color_config_occurrences(self, variables_of_config_color):
        """Counts how often a configuration color combination occurs.

        """
        return sum(variables_of_config_color)

    def _exactly_num_config_color(self, variables_of_config_color):
        """A constraint that is zero iff for each configuration color
        combination occurs as often as expected. Any other case is penalised.

        """
        return sum(
            (
                self._color_config_occurrences(variables)
                - self._problem.number_of_configuration_color_combinations[(config, color)]
            )**2
            for (config, color), variables in variables_of_config_color.items()
        )

    def shared_colors(self, position, non_singletons):
        return non_singletons[position].intersection(non_singletons[position+1])

    def predecessor_colors(self, position, non_singletons):
        return non_singletons[position].difference(non_singletons[position+1])

    def successor_colors(self, position, non_singletons):
        return non_singletons[position+1].difference(non_singletons[position])

    def _minimal_color_change(self, non_singletons):
        """A constraint that is zero iff two succeeding configurations have
        different colors. Any other case is penalised.

        """
        successors = [
            (position, position + 1)
            for position in non_singletons
            if position + 1 in non_singletons
        ]

        shared_colors_equal = sum(
            (self._position_color[(position, color)] \
             - self._position_color[(successor, color)]) ** 2
            for position, successor in successors
            for color in self.shared_colors(position, non_singletons)
        )

        penalise_single_color = sum (
            self._position_color[(position, color)]
            for position, _ in successors
            for color in self.predecessor_colors(position, non_singletons)
        )

        penalise_single_successor_color = sum (
            self._position_color[(successor, color)]
            for position, successor in successors
            for color in self.successor_colors(position, non_singletons)
        )

        return shared_colors_equal\
            + penalise_single_color\
            + penalise_single_successor_color

    def penalise_other_color(self, position, color):
        variable = self._position_color.get((position, color))
        if variable:
            return 1 - variable
        else:
            return 0

    def penalise_neightbours_of_singleton(self, singleton_position, color):
        return sum(
            self.penalise_other_color(neighbour, color)
            for neighbour in [
                    singleton_position - 1,
                    singleton_position + 1
            ]
        )


    def _single_color_config(self, singletons):
        """A constraint that is zero iff a configuration, that has exactly one
        color is preceeded and succeded by assignments of the same color.
        Any other case is penalised.
        """
        return sum(
            self.penalise_neightbours_of_singleton(position, color)
            for position, color in singletons.items()
        )

@dataclass
class SimpleQuboCreation(QuboCreation):
    exactly_one_color_weight: float
    exactly_num_config_color_weight: float
    minimal_color_changes_weigth: float
    single_color_config_weight: float

    def initialise(self, problem: Problem) -> SimpleQuboCreator:
        return SimpleQuboCreator(
            problem,
            self.exactly_one_color_weight,
            self.exactly_num_config_color_weight,
            self.minimal_color_changes_weigth,
            self.single_color_config_weight,
        )
