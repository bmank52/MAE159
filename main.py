import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import pandas as pd
from fontTools.merge.util import first

from approach_speed import iterate_W_S_approach
from Landing_Field_Length import iterate_W_S_LND
from Takeoff_field_length import takeoff_field_length
from Cruise_Thrust_Required import Cruise_Thrust_Required
from Service_Ceiling import service_ceiling
from Climb import climb_gradient
from Determine_performance_parameters import determine_performance_parameters

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
AR = 10
W_S_range = np.linspace(100, 150, 25)

determine_performance_parameters(W_S_guess, M_cruise, W_S_range, sweep, AR, Cdo)

M_cruise = 0.82
AR = 10
sweep = 35
Vapp = 130
TOFL = 6000
range = 3000
max_landing_fuel_ratio = 0.4


