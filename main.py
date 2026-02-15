import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import scipy as sp
import pandas as pd


from Determine_performance_parameters import determine_performance_parameters
from Converge_Mission import create_TW_WS_grid
from Span_Limit_Boundary import span_limit_boundary

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
Cdo = 0.015
n_eng = 2
ceiling_alt = 40000

### Input Ranges
W_S_guess = 140
sweep = 35
AR = 8
W_S_range = np.linspace(80, 150, 25)

determine_performance_parameters(W_S_guess, M_cruise, W_S_range, sweep, AR, Cdo)
W_S_range, T_W_range, W_TO_grid = create_TW_WS_grid(5, 5, 80, 150, .1, .7, sweep, AR)

CS = plt.contour(W_S_range, T_W_range, W_TO_grid.T, levels=25, cmap='viridis', linestyles='--')
plt.clabel(CS, inline=True, fontsize=10, fmt='%1.0f lbs')
plt.title(f'Constraint Diagram & $W_{{TO}}$ Contours (Sweep={sweep}, AR={AR})')


ws_span, tw_span = span_limit_boundary(W_S_range, T_W_range, W_TO_grid, AR)
uptick_effect = [path_effects.Normal(), path_effects.TickedStroke(angle=60, length=1, spacing=10)]
plt.plot(ws_span, tw_span, color='pink', linestyle='-', linewidth=2, label='Span Limit Boundary', path_effects=uptick_effect)
plt.ylim([0, .7])
plt.legend(loc='upper left')
plt.show()


