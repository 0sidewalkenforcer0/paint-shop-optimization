import argparse
import logging
from pathlib import Path
from mcmcpsp.directory import  Directory
from mcmcpsp.creation.integer_problem_instance_creation import IntegerProblemInstanceCreation
from mcmcpsp.names import IntegerNaming

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(
    description='Creates a number of problems, specified by the arguments and stores them to the data directory',
    formatter_class=argparse.MetavarTypeHelpFormatter,
    epilog='example: %(prog)s -f 5 -k 4 -l 10 -t 1 -d data'
    )
parser.add_argument('-f', '--colors', type=int, required=True, help='number of different colors')
parser.add_argument('-k', '--configurations', type=int, required=True, help='number of different configurations')
parser.add_argument('-l', '--carline', type=int, required=True, help='length of the carline')
parser.add_argument('-t', '--test_cases', type=int, required=True, help='number of test cases to create')
parser.add_argument('-d', '--directory', type=Path, required=True, help='path to the data directory')
args = parser.parse_args()

directory = Directory(args.directory)
creation = IntegerProblemInstanceCreation(args.configurations, args.colors, args.carline)
naming = IntegerNaming()

names = naming.newNames(args.test_cases, directory.fetchProblemNames())
test_cases = []
i = 1
for name in names:
    logging.info('create problem ' + name + ' (' + str(i) +' of ' + str(len(names)) + ')')
    test_cases.append((name, creation.createInstance()))
    i += 1
#test_cases = [(name, creation.createInstance()) for name in names]
directory.storeProblems(test_cases)
