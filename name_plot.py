import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
from query_to_df import query

def main():

    font = {'family': 'serif',
        'color':  'darkred',
        'weight': 'normal',
        'size': 16,
        }

    df = query()
    plt.plot(df['Year'], df['Qty'], ls='-', lw=2)
    plt.grid()
    plt.xlabel('Year', fontdict=font)
    plt.ylabel('Quantity', fontdict=font)
    plt.title('US Name Stats', fontdict=font)
    plt.show()


if __name__ == '__main__':
    main()
