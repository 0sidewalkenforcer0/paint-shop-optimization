import argparse
import logging
from pathlib import Path
from mcmcpsp.evaluation import Boxplot, Scatterplot, Lineplot, BestAlgorithm
from mcmcpsp.directory import Directory

logging.basicConfig (level=logging.INFO)

plots = { 
         "best": BestAlgorithm,
         "boxplot": Boxplot,
         "lineplot": Lineplot,
         "scatterplot": Scatterplot
        }

parser = argparse.ArgumentParser(
    description='Retrieves solutions from the data directory, evaluates them with the given plot and stores the plot as file',
    formatter_class=argparse.MetavarTypeHelpFormatter,
    epilog='example: %(prog)s -p random greedy qbsolv -d data'
    )
parser.add_argument('-p', '--plot', type=str, required=True, choices=plots.keys(), help='plot type to use for plotting')
parser.add_argument('-d', '--directory', type=Path, required=True, help='path to data directory')
parser.add_argument('-o', '--output', type=Path, required=True, help='filename for graph')
args = parser.parse_args()

directory = Directory(Path(args.directory))

plotting = plots[args.plot](args.output)
solutions = directory.fetchSolutions()
plotting.evaluate([s for _, s in solutions])
