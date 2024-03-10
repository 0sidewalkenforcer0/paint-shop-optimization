from cProfile import label
from datetime import date
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def plot(d1, d2, d3, num, num_Of_Ident_Cars):
    all_Together = {'Red first': d1, 'Greedy': d2, 'Greedy recursive': d3, 'x': [int(x) for x in range(6, num, num_Of_Ident_Cars)]}

    df = pd.DataFrame(all_Together)
    fig, ax = plt.subplots()
    ax = sns.lineplot(x = 'x', y='Red first', label= 'Red first', data=df)
    ax.set_xlabel('Length of sequence')
    ax.set_ylabel('Colour swaps')
    ax1 = sns.lineplot(x = 'x', y='Greedy', label= 'Greedy', data=df)
    ax2 = sns.lineplot(x = 'x', y='Greedy recursive', label= 'Greedy recursive', data=df)
    plt.legend()
    plt.show()
