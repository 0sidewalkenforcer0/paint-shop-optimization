import numpy as np

class redFirst():

    def __init__(self):
        pass

    def findSolution(self, sequence, num_Of_Ident_Cars):

        swaps = 0
        colour_used = 0
        colour_sequence = np.empty(0)
        pairs = np.array([0 for x in range(int(len(sequence)/num_Of_Ident_Cars))])

        for i in range(len(sequence)):
            if pairs[sequence[i]] % 2 == 0:
                colour_sequence = np.append(colour_sequence, 0)
                pairs[sequence[i]] += 1
            else:
                colour_sequence = np.append(colour_sequence, 1)
                pairs[sequence[i]] += 1
            
            
        for i in range(1, int(len(colour_sequence))):
            if colour_sequence[i] != colour_sequence[i-1]:
                swaps += 1

        return colour_sequence, swaps
        


       
