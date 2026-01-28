import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def file_plot_type_1 (f, xLabel, yLabel, title, deg):   #Plots and creates polyfit for each curve for functions where x has 1 output y
    plt.figure()

    f_df = pd.read_csv(f, header = None)
    data_header = [] #Used for graphs with more than one data set such as sweep on fig 1b
    for name in f_df.iloc[0]:  # Looks through the first row, which contains all of the sweep labels
        if pd.notna(name):  # If the name is not NaN
            (data_header.append(name))

    for i in range(len(data_header)):
        #plotting
        n = 2 * i  # 2 Columns of data per sweep value
        X = pd.to_numeric(f_df.iloc[2:, n]).dropna()  # to_numeric converts the data from a string to a number
        Y = pd.to_numeric(f_df.iloc[2:, n + 1]).dropna()

        plt.plot(X, Y, label=data_header[i])

        #poly fit
        coeffs = np.polyfit(X, Y, deg)  # takes inputs X, Y, degree polynomial
        plt_coeffs = np.poly1d(coeffs)
        plt.plot(X, plt_coeffs(X))
        print(data_header[i], coeffs)


    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(title)
    plt.legend()
    plt.show()


def file_plot_type_2 (f, xLabel, yLabel, title, deg):   #Plots and creates polyfit for each curve for functions where x has 1 output y
    plt.figure()

    f_df = pd.read_csv(f, header = None)
    data_header = [] #Used for graphs with more than one data set such as sweep on fig 1b
    for name in f_df.iloc[0]:  # Looks through the first row, which contains all of the sweep labels
        if pd.notna(name):  # If the name is not NaN
            (data_header.append(name))

    for i in range(len(data_header)):
        #plotting
        n = 2 * i  # 2 Columns of data per sweep value
        X = pd.to_numeric(f_df.iloc[2:, n]).dropna()  # to_numeric converts the data from a string to a number
        Y = pd.to_numeric(f_df.iloc[2:, n + 1]).dropna()

        plt.plot(Y, X, label=data_header[i])

        #poly fit
        coeffs = np.polyfit(Y, X, deg)  # takes inputs X, Y, degree polynomial
        plt_coeffs = np.poly1d(coeffs)
        plt.plot(Y, plt_coeffs(Y))
        print(data_header[i], coeffs)


    plt.xlabel(yLabel)
    plt.ylabel(xLabel)
    plt.title(title)
    plt.legend()
    plt.show()


#file_plot_type_1('Plots/Fig 1B.csv', 'M_Div', 't/c', 'Fig 1B', 3)
#file_plot_type_2('Plots/Fig 2.csv', 'M_Div', 'C_L', 'Fig 2', 3)
#file_plot_type_1('Plots/Fig 3.csv', 'Sweep, t/c, AR', 'C_L', 'Fig 3', 3)
#file_plot_type_1('Plots/Fig 4.csv', 'All out Range', 'Wf/W', 'Fig 4', 4)
#file_plot_type_2('Plots/Fig 5.csv', 'W/S * T/W', 'TOFL', 'Fig 5', 3)
#file_plot_type_2('Plots/Fig 6.csv', 'Delta CDp', 'Cl/CLmax', 'Fig 6', 3)
#file_plot_type_1('Plots/Fig 3B.csv', 't/c', 't/c', 'Fig 3B', 3)
#file_plot_type_2('Plots/JT9D 15k.csv', 'Mach', 'Thrust (1k lbs)', 'JT9D 15kft', 3)
#file_plot_type_2('Plots/JT9D 35k.csv', 'Mach', 'Thrust (1k lbs)', 'JT9D 35kft', 3)
#file_plot_type_1('Plots/JT9D_SL.csv', 'Mach', 'Thrust (1k lbs)', 'JT9D Sea Level', 3)
file_plot_type_1('Plots/JT9D_Max_Thrust_Conditions.csv', 'Mach', 'Thrust (1k lbs)', 'JT9D Max Thrust 35k ft', 4)
file_plot_type_1('Plots/JT9D_45000 ft.csv', 'Mach', 'Thrust (1k lbs)', 'JT9D 45k ft', 4)
file_plot_type_1('Plots/JT9D Max Thrust 15k.csv', 'Mach', 'Thrust (1k lbs)', 'JT9D 15k ft Max Thrust', 4)