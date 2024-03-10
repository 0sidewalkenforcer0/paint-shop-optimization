import numpy as np

class greedy():

    def __init__(self):
        pass

    def findSolution(self, sequence, num_Of_Ident_Cars):
        colour_used = 0
        pairs = np.array([None for x in range(int(len(sequence)/num_Of_Ident_Cars))])
        swaps = 0
        paint_Sequence = np.empty(0)
        
        for i in range(len(sequence)):
            if pairs[sequence[i]] == colour_used:
                colour_used = 1 if colour_used == 0 else 0
                pairs[sequence[i]] = colour_used
                swaps += 1
            else:
                pairs[sequence[i]] = colour_used
            paint_Sequence = np.append(paint_Sequence, colour_used)

        return paint_Sequence, swaps