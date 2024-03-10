import numpy as np
import time
import sys
from greedy import greedy
from redFirst import redFirst
from sequence import sequence
from recursiveGreedy import recursiveGreedy
from plotting import plot

class main():

    def __init__(self, total):
        ## Classes ##
        self.greedy = greedy()
        self.red_First = redFirst()
        self.recursive_Greedy = recursiveGreedy()
        self.sequence = sequence()

        ## Plot arrays ##
        self.times_Red_First = np.empty(0)
        self.times_Greedy = np.empty(0)
        self.times_Greedy_Recursive = np.empty(0)

        self.swaps_Red_First = np.empty(0)
        self.swaps_Greedy = np.empty(0)
        self.swaps_Greedy_Recursive = np.empty(0)

        ## Vars ##
        self.totalLength = total

    def doRunWithDifferentModels(self):
        
        self.doRun(2)
        self.reset()

    def doRun(self, num_Of_Ident_Cars):
        for i in range(6 ,self.totalLength, num_Of_Ident_Cars):
            sequence = self.sequence.getSequence(i, num_Of_Ident_Cars)

            start = time.time_ns()
            self.callRedFirst(sequence, num_Of_Ident_Cars)
            end = time.time_ns()
            self.times_Red_First = np.append(self.times_Red_First, (end - start))

            start = time.time_ns()
            self.callGreedy(sequence, num_Of_Ident_Cars)
            end = time.time_ns()
            self.times_Greedy = np.append(self.times_Greedy, (end - start))

            start = time.time_ns()
            self.callRecursiveGreedy(sequence, num_Of_Ident_Cars)
            end = time.time_ns()
            self.times_Greedy_Recursive = np.append(self.times_Greedy_Recursive, (end - start))
        
        print(self.swaps_Greedy)
        print(self.swaps_Greedy_Recursive)
        plot(self.swaps_Red_First, self.swaps_Greedy, self.swaps_Greedy_Recursive, self.totalLength, num_Of_Ident_Cars)
        



    def callGreedy(self, sequence, num_Of_Ident_Cars):
        paint_Sequence, swaps = self.greedy.findSolution(sequence, num_Of_Ident_Cars)
        self.swaps_Greedy = np.append(self.swaps_Greedy, swaps)

    def callRedFirst(self, sequence, num_Of_Ident_Cars):
        paint_Sequence, swaps = self.red_First.findSolution(sequence, num_Of_Ident_Cars)
        self.swaps_Red_First = np.append(self.swaps_Red_First, swaps)

    def callRecursiveGreedy(self, sequence, num_Of_Ident_Cars):
        paint_sequence, swaps = self.recursive_Greedy.findSolution(sequence, num_Of_Ident_Cars)
        self.swaps_Greedy_Recursive = np.append(self.swaps_Greedy_Recursive, swaps)
    
    def reset(self):
        self.times_Red_First = np.empty(0)
        self.times_Greedy = np.empty(0)
        self.times_Greedy_Recursive = np.empty(0)

        self.swaps_Red_First = np.empty(0)
        self.swaps_Greedy = np.empty(0)
        self.swaps_Greedy_Recursive = np.empty(0)
        
## Pass num of total runs (max length of sequence) as integer ##

prog = main(int(sys.argv[1]))
prog.doRunWithDifferentModels()



