import numpy as np


class sequence():

    def __init__(self):
        pass


    def getSequence(self, length, num_Of_Ident_Cars):
        y = np.array([y for y in range(int(length/num_Of_Ident_Cars))])
        x = np.array([y[x % int(length/num_Of_Ident_Cars)] for x in range(length)])
        sequence = np.empty(0, dtype=int)
        for i in range(length):
            p = np.random.randint(0, len(x))
            sequence = np.append(sequence, x[p])
            x = np.delete(x, p)
        return sequence
