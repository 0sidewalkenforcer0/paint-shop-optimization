# Multi Car Multi Color Paintshop Optimization

The Multi Car Multi Color Paintshop Problem (MCMCPSP) describes the problem, to assign colors to a production car line such, that the number of color changes is minimal.

The scope of this python project is to...
- [create](#creation) such problems
- [solve](#solving) these problems by using classical, as well as quantum computing algorithms 
- [evaluate](#evaluation) the solutions by plotting the results into graphs

## Poetry

This project uses [Poetry](https://python-poetry.org) as dependency management and packaging tool.
The installation procedure is described [here](https://python-poetry.org/docs/master/#installing-with-the-official-installer)

With poetry it is possible to run the project with all its dependencies in a virtual environment, independent from the packages and versions installed on the main system. 

Once Poetry is installed, you can use the following commands:
```
poetry install
```
will install all dependencies for the first time and create a poetry.lock file
```
poetry update
```
will update all packages

```
poetry shell
```
will switch to the virtual environment 

Further information about poetry and how to use it can be also found in its [documentation](https://python-poetry.org/docs/master/)

## Creation
```
python creation.py -f [COLORS] -k [CONFIGURATIONS] -l [LINE_LENGTH] -t [PROBLEM_SETS] -d [DATA_DIRECTORY]
```

This part creates a number of problem sets, where the first three arguments specify the structure of the problem
- f number of available colors for each configuration (car)
- k number of available configurations (different car types)
- l length of the production car line

The information about how many problem sets to create and where to store them is specified by the remaining two arguments
- t number of problem sets
- d path to the data directory

Example:
```
python creation.py -f 3 -k 5 -l 20 -t 4 -d data
```

will create 4 different problem sets, each consisting of a car line with the length of 20 randomly assigned configurations.
Each of the 5 available configurations gets a random subset of the 3 possible colors assigned and is represented at least once in the car line. 
Each color is assigned at least to one configuration.

Those problems are then stored as json files into the folder ./data/problems/ 


## Solving
```
python solving.py -a [ALGORITHMS] -d [DATA_DIRECTORY]
```

This part solves each problem with each given algorithm and stores the solutions to the data directory, both specified by the arguments 
- a list of solving algorithms
- d path to the data directory

Currently there are 5 algorithms available:
- random Assigns each configuration an available color randomly
- greedy Will assign one color to each configuration as long as possible and then switch to the next available color
- qbsolv Simulates quantum annealing to find an optimal assignment of colors
- dwave Uses the D-Wave quantum annealing computer to find an optimal assignment of colors
- fujitsu Uses the Fujitsu quantum annealing computer to find an optimal assignment of colors

Each algorithm will assign colors in such way, that every hard constraint will hold.

Example:
```
python solving.py -a random greedy qbsolv dwave fujitsu -d data
```

will retrieve all problems from ./data/problems/ and solve each problem with every given algorithm.
The solutions will be stored in ./data/solutions/

Since every problem is solved with each algorithm, the number of solution files is n-times the number of problem files, where n is the number of algorithms.

## Evaluation
```
python evaluation.py -p [PLOT_TYPE] -d [DATA_DIRECTORY] -o [FILE]
```

This part retrieves all solutions from the data directory and plots the result to one file, specified by the arguments
- p plot type to use for the evaluation
- d path to the data directory
- o filename for the graph

Currently there are 4 plot types available:
- best Comparision of the results grouped by algorithm sorted by the number of color changes
- boxplot Comparision of the results grouped by algorithm 
- lineplot Percentual comparision of the algorithms to the random assignment
- scatterplot Energy plot for each solution

Example:
```
python evaluation.py -p lineplot -d data -o line.png
```

will retrieve all solutions from ./data/solutions/, plot the results in a lineplot, and store that plot into ./line.png
