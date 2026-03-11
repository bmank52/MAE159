import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects


from Determine_performance_parameters import determine_performance_parameters
from Converge_Mission import create_TW_WS_grid
from PayloadVsRangePlot import h_cruise
from Span_Limit_Boundary import span_limit_boundary

### Design Specs ###
n_pax = 150
cargo_weight = 10000 #lbs
range = 3000 #nm
field_length = 9000 #ft hot day
landing_approach_speed = 140 #kts
M_cruise = 0.82
cruise_alt = 35000 #ft
max_landing_fuel_ratio = 0.25
b_limit = 214 #ft
temp_delta = 22.6 #hot day added temp in K
Cdo = 0.015
n_eng = 2
ceiling_alt = 40000

### Input Ranges
W_S_guess = 90
sweep = 30
AR = 8
W_S_range = np.linspace(80, 150, 25)

determine_performance_parameters(W_S_guess, M_cruise, W_S_range, sweep, AR, Cdo, range)
W_S_range, T_W_range, W_TO_grid = create_TW_WS_grid(5, 5, 80, 150, .1, .7, sweep, AR, range, M_cruise, h_cruise, 0.35, cargo_weight, n_pax)

CS = plt.contour(W_S_range, T_W_range, W_TO_grid.T, levels=25, cmap='viridis', linestyles='--')
plt.clabel(CS, inline=True, fontsize=10, fmt='%1.0f lbs')
plt.title(f'Constraint Diagram & $W_{{TO}}$ Contours (Sweep={sweep}, AR={AR})')


ws_span, tw_span = span_limit_boundary(W_S_range, T_W_range, W_TO_grid, AR)
uptick_effect = [path_effects.Normal(), path_effects.TickedStroke(angle=60, length=1, spacing=10)]
plt.plot(ws_span, tw_span, color='pink', linestyle='-', linewidth=2, label='Span Limit Boundary', path_effects=uptick_effect)
plt.ylim([0, .7])
plt.legend(loc='upper left')
plt.show()


