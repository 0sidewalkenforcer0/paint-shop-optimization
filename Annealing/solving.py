import argparse
import logging
import time
from pathlib import Path

from uqo.client.config import Config
from joblib import Parallel, delayed
from multiprocessing import Process, Manager, Lock

from mcmcpsp.directory import Directory, PROBLEM_NAME_KEY
from mcmcpsp.solvers import RandomSolver, GreedySolver, QuantumAnnealingSolver,\
    ColorChangeTrackingSolver, InvalidColorTrackingSolver, InvalidNumColors
from mcmcpsp.samplers import QBSolvSampler, DWaveSampler, FujitsuSampler
from mcmcpsp.qubo import AdaptiveWeightsQuboCreation
from mcmcpsp.names import IntegerNaming

logging.basicConfig(level=logging.INFO)

config = Config(configpath="./config.json")

manager = Manager()
qubo = AdaptiveWeightsQuboCreation()

algorithms = {
    "random": RandomSolver(),
    "greedy": GreedySolver(),
    "qbsolv": QuantumAnnealingSolver(
        "qbsolv",
        QBSolvSampler(),
        qubo,
    ),
    "dwave": QuantumAnnealingSolver(
        "dwave",
        DWaveSampler(lock=manager.Lock(), cached_embedding=manager.dict(), config=config),
        qubo,
    ),
    "fujitsu": QuantumAnnealingSolver(
        "fujitsu",
        FujitsuSampler(config),
        qubo,
    )
}

parser = argparse.ArgumentParser(
    description='Retrieves problems from the data directory, solves them with the given algorithms and stores the solutions to the data directory',
    formatter_class=argparse.MetavarTypeHelpFormatter,
    epilog='example: %(prog)s -a random greedy qbsolv -d data'
    )
parser.add_argument('-a', '--algorithm', type=str, required=True, choices=algorithms.keys(), nargs='+', help='algorithm(s) to solve the problem')
parser.add_argument('-d', '--directory', type=Path, required=True, help='path to the data directory')
parser.add_argument('-r', '--repeat', type=int, default=1, help='repeat solving for n times')
args = parser.parse_args()


solvers = []


for algorithm in args.algorithm:
    solver = InvalidNumColors(
        InvalidColorTrackingSolver(
            ColorChangeTrackingSolver(algorithms[algorithm])
        )
    )
    solvers.append(solver)


def computing(func_solver, name, func_problem, q):
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('dwave.cloud.client.base').propagate = False
    try:
        solution = func_solver.solve(func_problem, name=name)
        solution.gathered_data[PROBLEM_NAME_KEY] = name
        q.put(solution)
    except Exception as e:
        logging.exception(repr(e))


def parallel_computing(q, solvers, directory):
    Parallel(n_jobs=3)\
        (delayed(computing)(solver, name, problem, q)
         for _ in range(args.repeat)
         for name, problem in directory.fetchProblems()
         for solver in solvers
         )


def parallel_storing(q, directory):
    naming = IntegerNaming()
    existing_names= set(directory.fetchSolutionNames())
    while True:
        new_solution = q.get()
        if new_solution is None:
            break
        name = naming.newNames(1, existing_names).pop()
        existing_names.add(name)
        directory.storeSolutions([(name, new_solution)])


if __name__ == "__main__":
    directory = Directory(Path(args.directory))

    q = manager.Queue(maxsize=0)

    start = time.time()

    problems = directory.fetchProblems()
    storing = Process(target=parallel_storing, args=(q, directory))
    storing.start()

    parallel_computing(q, solvers, directory)

    q.put(None)
    storing.join()

    end = time.time()
    print('{:.4f} s'.format(end-start))
