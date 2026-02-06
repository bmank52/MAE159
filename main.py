import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import pandas as pd
from approach_speed import iterate_W_S_LND

### Design Specs ###
n_pax = 250
cargo_weight = 12000 #lbs
range = 7000 #nm
field_length = 9000 #ft hot day
landing_approach_speed = 140 #kts
M_cruise = 0.85
cruise_alt = 35000 #ft
max_landing_fuel_ratio = 0.45
b_limit = 214 #ft
temp_delta = 22.6 #hot day added temp in K

### Input Ranges
W_S = 140
sweep = 35
AR = 10

### Constraint Diagram
plt.figure()
W_S_Approach = iterate_W_S_LND(W_S, M_cruise, sweep, AR, landing_approach_speed, temp_delta, 0)

plt.axvline(x = W_S_Approach, color = 'red', label = 'Approach')

plt.legend()
plt.xlabel('W_S')
plt.ylabel('T_W')
plt.show()

