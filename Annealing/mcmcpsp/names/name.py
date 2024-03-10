from abc import ABC, abstractmethod
from typing import Iterable, Set


class Naming(ABC):
    """Creates new names that have not yet appeared.

    """
    @abstractmethod
    def newNames(self, count: int, names: Iterable[str]) -> Set[str]:
        pass
