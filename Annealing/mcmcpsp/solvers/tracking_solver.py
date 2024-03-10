from .solver import Solver

class TrackingSolver(Solver):
    """Abstract class for wrapping solvers to gather data.

    In general a subclass invokes its internal solver to compute a solution. In
    addition, it can store some data about the solution (e.g. energy), or the
    computation itself (runtime).

    """
    def __init__(self, internal: Solver):
        self._internal = internal
