import matplotlib.pyplot as plt
import pandas as pd

def file_plot (f, xLabel, yLabel, title):
    plt.figure()

    f_df = pd.read_csv(f, header = None)
    data_header = [] #Used for graphs with more than one data set such as sweep on fig 1b
    for name in f_df.iloc[0]:  # Looks through the first row, which contains all of the sweep labels
        if pd.notna(name):  # If the name is not NaN
            (data_header.append(name))

    for i in range(len(data_header)):
        n = 2 * i  # 2 Columns of data per sweep value
        X = pd.to_numeric(f_df.iloc[2:, n])  # to_numeric converts the data from a string to a number
        Y = pd.to_numeric(f_df.iloc[2:, n + 1])

        plt.plot(X, Y, label=data_header[i])

    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.legend()
    plt.show()


file_plot('Plots/Fig 1B.csv', 'M_Div', 't/c', 'Fig 1B')
file_plot('Plots/Fig 2.csv', 'M_Div', 'C_L', 'Fig 2')
file_plot('Plots/Fig 3.csv', 'Sweep, t/c, AR', 'C_L', 'Fig 3')
file_plot('Plots/Fig 4.csv', 'All out Range', 'Wf/W', 'Fig 4')
file_plot('Plots/Fig 5.csv', 'W/S * T/W', 'TOFL', 'Fig 5')
file_plot('Plots/Fig 6.csv', 'Delta CDp', 'Cl/CLmax', 'Fig 6')