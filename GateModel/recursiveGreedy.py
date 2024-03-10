import numpy as np
import copy
from pyparsing import col

from sklearn.metrics import jaccard_score
class recursiveGreedy():

    def __init__(self) -> None:
        pass

    def findSolution(self, sequence, num_Of_Ident_Cars):

        target_Sequence = np.array([None for x in range((int(len(sequence))))])
        temp_Sequences = np.array([sequence for x in range(int(len(sequence)/num_Of_Ident_Cars))])
        colour_used = 0
        swaps = 0

        ## Create arrays with consecutively removed pairs ##
        for i in range(1,int(len(sequence)/2)):
            if i == 1:
                temp = copy.deepcopy(temp_Sequences[i])
            else:
                temp = copy.deepcopy(temp_Sequences[i-1])

            q = int(len(sequence)) - 1
            not_Found = True
            while not_Found:
                if temp[q] != -1:
                    car = temp[q]
                    temp[q] = -1
                    not_Found = False
                q -= 1

            for p in range(len(temp)):
                if temp[p] == car:
                    temp[p] = -1
            temp_Sequences[i] = temp
        
        ## Setting the first pair ##
        for i in range(int(len(sequence))):
            if temp_Sequences[-1][i] != -1:
                target_Sequence[i] = colour_used
                colour_used = 1 if colour_used == 0 else 0

        ## Rules for all other possibilities ##

        pairs = np.array([None for x in range(int(len(sequence)/num_Of_Ident_Cars))])

        for i in range(int(len(temp_Sequences))-2, -1, -1):
            for p in range(len(target_Sequence)):
                if target_Sequence[p] != None:
                    colour_used = target_Sequence[p]
                    break

            for j in range(len(temp_Sequences[i])):
                if target_Sequence[j] != None:
                    colour_used = target_Sequence[j]
                if target_Sequence[j] == None and temp_Sequences[i][j] != -1:
                    if pairs[temp_Sequences[i][j]] == colour_used:
                        colour_used = 1 if colour_used == 0 else 0
                        pairs[temp_Sequences[i][j]] = colour_used
                    else:
                        pairs[temp_Sequences[i][j]] = colour_used
                    target_Sequence[j] = colour_used

            


        # for i in range(int(len(temp_Sequences))-2, -1, -1):
        #     colour = None
        #     for j in range(int(len(temp_Sequences[i]))):
        #         if target_Sequence[j] == None and temp_Sequences[i][j] != -1:
        #             if colour != None: ## Another was selected
        #                 target_Sequence[j] = 1 if colour == 0 else 0
        #             elif j == 0: ## first element
        #                 if target_Sequence[j+1] != None:
        #                     target_Sequence[j] = target_Sequence[j+1]
        #                 else:
        #                     target_Sequence[j] = 0
        #                 colour = target_Sequence[j]

        #             elif j == int(len(temp_Sequences[i]))-1: ## last element
        #                 target_Sequence[j] = target_Sequence[j-1]
        #                 colour = target_Sequence[j]
        #             elif j > 0:  ## Other cases

        #                 if target_Sequence[j-1] == None and target_Sequence[j+1] != None:
        #                     target_Sequence[j] = target_Sequence[j+1]
        #                     colour = target_Sequence[j]
        #                 elif target_Sequence[j-1] != None and target_Sequence[j+1] == None:
        #                     target_Sequence[j] = target_Sequence[j-1]
        #                     colour = target_Sequence[j]
        #                 elif target_Sequence[j-1] == target_Sequence[j+1] and target_Sequence[j-1] != None: ## Surrounded by the same colour
        #                     target_Sequence[j] = target_Sequence[j-1]
        #                     colour = target_Sequence[j]
        #                 elif target_Sequence[j-1] != target_Sequence[j+1]: ## Different colours
        #                     target_Sequence[j] = target_Sequence[j+1]
        #                     colour = target_Sequence[j]
        #                 else:
        #                     target_Sequence[j] = 0
        #                     colour = target_Sequence[j]
                            

        for i in range(1,int(len(target_Sequence))):
            if target_Sequence[i-1] != target_Sequence[i]:
                swaps += 1


        return target_Sequence, swaps
                