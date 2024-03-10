from dataclasses import dataclass
from typing import List, Dict, Generic, Any

from .problem import Problem, Color, Config


@dataclass
class Solution(Generic[Color, Config]):
    problem : Problem[Color, Config]
    assignments : List[Color]
    algorithm : str
    gathered_data : Dict[str, Any]

    def __eq__(self, other) -> bool:
        if not isinstance(other, Solution):
            return False

        return all([
            self.problem == other.problem,
            self.assignments == other.assignments,
            self.algorithm == other.algorithm,
            self.gathered_data == other.gathered_data,
        ])
