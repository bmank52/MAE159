from scipy.constants import atmosphere
import numpy as np
from Mdd_constraint import Mdd_constraint
from fuel_weight_ratio_estimate import fuel_weight_ratio_estimate
from ambiance import Atmosphere

def calc_W_S_new(W_S, M_cruise, sweep, AR, Vap, density, alt): #input temp_delta for degrees C different than standard
    CL_max_Lnd = Mdd_constraint(W_S, M_cruise, alt, sweep, AR)[1]
    W_S_Lnd = 0.5 * density * CL_max_Lnd * (Vap/1.3) ** 2
    W_S = W_S_Lnd * 1 / (1-(1-0.45) * fuel_weight_ratio_estimate(7000, M_cruise, alt))
    return W_S

def iterate_W_S_LND(W_S, M_cruise, sweep, AR, Vap, temp_delta, alt): #input Vap in kts, temp_delta for degrees C different than standard
    Vap = Vap * 1.68781 #converts to ft/s
    densityHot = Atmosphere(0).pressure[0] / 287 / (Atmosphere(0).temperature[0] + temp_delta) * 0.00194032  # convert to lbf/ft^3
    W_S_new = calc_W_S_new(W_S, M_cruise, sweep, AR, Vap, densityHot, alt)
    while(np.abs(W_S_new - W_S) > 0.0001):
        W_S = W_S_new
        W_S_new = calc_W_S_new(W_S, M_cruise, sweep, AR, Vap, densityHot, alt)
    return W_S_new

print(iterate_W_S_LND(130, 0.85, 35, 8, 140, 22.8, 35000))

