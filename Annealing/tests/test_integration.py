from mcmcpsp.creation import IntegerProblemInstanceCreation
from mcmcpsp.solvers import RandomSolver, GreedySolver, QuantumAnnealingSolver
from mcmcpsp.qubo import SimpleQuboCreation

from mcmcpsp.problem import Problem
from mcmcpsp.solution import Solution


from hypothesis import given
from hypothesis.strategies import integers, composite
from neal import SimulatedAnnealingSampler

MAX_CONFIG = 10
MAX_COLOR = 10
MAX_CAR_LINE = 100


@composite
def integer_problem_instance(draw,
                             max_config: int = MAX_CONFIG,
                             max_color: int = MAX_COLOR,
                             max_car_line: int = MAX_CAR_LINE,
                             ) -> Problem:
    
    configuration_set_length = draw(integers(1, max_config))
    colors_set_length = draw(integers(1, max_color))
    min_carLine = colors_set_length
    if configuration_set_length > colors_set_length:
        min_carLine = configuration_set_length
    carLine_length = draw(integers(min_carLine, max_car_line))
    problem_instance_creation = IntegerProblemInstanceCreation(configuration_set_length, colors_set_length, carLine_length)
    instance = problem_instance_creation.createInstance()
    
    return instance

@composite
def integer_solution(draw) -> Solution:
    problem = draw(integer_problem_instance())
    return RandomSolver().solve(problem)


@given(integer_problem_instance())
def test_random_solver(instance: Problem):
    solver = RandomSolver()
    solver.solve(instance)


@given(integer_problem_instance())
def test_greedy_solver(instance: Problem):
    solver = GreedySolver()
    solver.solve(instance)


@given(integer_problem_instance())
def test_simple_qubo_solver(instance: Problem):
    qubo = SimpleQuboCreation(1.0, 1.0, 1.0)
    sampler = SimulatedAnnealingSampler()
    solver = QuantumAnnealingSolver(sampler, qubo)
    solver.solve(instance)
