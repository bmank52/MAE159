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



#climb gradients
first_TO_climb = {
    "V_Vstall": 1.2,
    "Gear": True,
    "Flaps": "TO",
    "alt": 0,
    "Weight": "MTOW",
    "OEI": True,
    "climb_gradient_2_eng": 0,
    "climb_gradient_3_eng": 0.3,
    "climb_gradient_4_eng": 0.5,
}

second_TO_climb = {
    "V_Vstall": 1.2,
    "Gear": False,
    "Flaps": "TO",
    "alt": 0,
    "Weight": "MTOW",
    "OEI": True,
    "climb_gradient_2_eng": 2.4,
    "climb_gradient_3_eng": 2.7,
    "climb_gradient_4_eng": 3.0,
}

third_TO_climb = {
    "V_Vstall": 1.2,
    "Gear": False,
    "Flaps": False,
    "alt": 1000,
    "Weight": "MTOW",
    "OEI": True,
    "climb_gradient_2_eng": 1.2,
    "climb_gradient_3_eng": 1.5,
    "climb_gradient_4_eng": 1.7,
}

approach_go_around = {
    "V_Vstall": 1.4,
    "Gear": False,
    "Flaps": "TO",
    "alt": 0,
    "Weight": "MLNDW",
    "OEI": True,
    "climb_gradient_2_eng": 2.1,
    "climb_gradient_3_eng": 2.4,
    "climb_gradient_4_eng": 2.7,
}

Landing_go_around = {
    "V_Vstall": 1.3,
    "Gear": True,
    "Flaps": "LND",
    "alt": 0,
    "Weight": "MLNDW",
    "OEI": False,
    "climb_gradient_2_eng": 3.2,
    "climb_gradient_3_eng": 3.2,
    "climb_gradient_4_eng": 3.2,
}

### Constraint Diagram
plt.figure()
W_S_Approach = iterate_W_S_approach(W_S, M_cruise, sweep, AR, landing_approach_speed, temp_delta, 0)

plt.axvline(x = W_S_Approach, color = 'red', label = 'Approach')

plt.legend()
plt.xlabel('W_S')
plt.ylabel('T_W')
plt.show()


M_cruise = 0.82
AR = 10
sweep = 35
Vapp = 130
TOFL = 6000
range = 3000
max_landing_fuel_ratio = 0.4

#print(iterate_W_S_approach(W_S, M_cruise, sweep, AR, Vapp))
#print(iterate_W_S_LND(W_S, M_cruise, sweep, AR, 0, 0.015, TOFL))
print(takeoff_field_length(W_S, sweep, AR, 2, M_cruise, cruise_alt, range, TOFL))
print(Cruise_Thrust_Required(W_S, AR, M_cruise))
print(service_ceiling(W_S, 40000, cruise_alt, AR, M_cruise))
print(climb_gradient(W_S, first_TO_climb, range, AR, sweep, M_cruise))
print(climb_gradient(W_S, approach_go_around, range, AR, sweep, M_cruise))
