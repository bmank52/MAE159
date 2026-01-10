import matplotlib.pyplot as plt
import pandas as pd

fig1b_df = pd.read_csv('Plots/Fig 1B.csv', header = None)
#fig1b_parsed_data = {} # Make a dictionary to store the data after it is parsed

sweep_names = []
for name in fig1b_df.iloc[0]:  # Looks through the first row, which contains all of the sweep labels
    if pd.notna(name):   # If the name is not NaN
        sweep_names.append(name)


plt.figure()
for i in range(len(sweep_names)):
    n = 2 * i # 2 Columns of data per sweep value
    mach = pd.to_numeric(fig1b_df.iloc[2:, n])   #to_numeric converts the data from a string to a number
    t_c = pd.to_numeric(fig1b_df.iloc[2:, n + 1])

    plt.plot(mach, t_c, label = sweep_names[i])

plt.legend()
plt.xlabel('M_Div')
plt.ylabel('t/c')
plt.title('Fig 1B')
plt.show()
