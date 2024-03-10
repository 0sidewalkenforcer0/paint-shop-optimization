from .name import Naming
from typing import Iterable, Set


class IntegerNaming(Naming):
    """Creates new names that have not yet appeared by counting from the highest
    found integer.

    """
    def newNames(self, count: int, names: Iterable[str]) -> Set[str]:
        max_num = 0
        for n in names:
            if int(n) > max_num:
                max_num = int(n)
        new_name_set = set()
        for name_num in range(count):
            new_name = max_num + name_num + 1
            new_name_set.add(str(new_name))
        return new_name_set
