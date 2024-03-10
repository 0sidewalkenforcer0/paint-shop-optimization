from typing import List, Dict, Set, Tuple, Generic, TypeVar
from collections import defaultdict
from functools import cached_property


Color = TypeVar("Color")
Config = TypeVar("Config")


class Problem(Generic[Color, Config]):
    def __init__(
            self,
            colors: Set[Color],
            configurations: Set[Config],
            carLine: List[Config],
            number_of_configuration_color_combinations : Dict[Tuple[Config, Color], int]
            ):
        assert all(color in colors
                   for _, color in number_of_configuration_color_combinations)

        assert all(config in configurations
                   for config, _ in number_of_configuration_color_combinations)

        assert all(config in configurations
                   for config in carLine)

        self._colors = colors
        self._configurations = configurations
        self._carLine = carLine
        self._number_of_configuration_color_combinations = \
            number_of_configuration_color_combinations

    @property
    def colors(self) -> Set[Color]:
        return self._colors

    @property
    def configurations(self) -> Set[Config]:
        return self._configurations

    @property
    def carLine(self) -> List[Config]:
        return self._carLine

    @property
    def number_of_configuration_color_combinations(self) -> Dict[Tuple[Config, Color], int]:
        return self._number_of_configuration_color_combinations

    @cached_property
    def colors_of_configuration(self) -> Dict[Config, Set[Color]]:
        assignment = defaultdict(set)
        dictionary = self.number_of_configuration_color_combinations
        for config, color in dictionary:
            if (dictionary[config, color] != 0):
                assignment[config].add(color)
        return assignment

    @cached_property
    def colors_of_car_line(self) -> List[Set[Color]]:
        return [self.colors_of_configuration[config] for config in self.carLine]

    @cached_property
    def single_color_configurations(self) -> Dict[Config, Color]:
        return {
            config: colors.pop()
            for config, colors in self.colors_of_configuration.items()
            if len(colors) == 1
        }

    def __eq__(self, other):
        if not isinstance(other, Problem):
            return False

        return all([
            self.colors == other.colors,
            self.configurations == other.configurations,
            self.carLine == other.carLine,
            self.number_of_configuration_color_combinations \
                == other.number_of_configuration_color_combinations,
        ])
