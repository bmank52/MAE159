from Mdd_constraint import Mdd_constraint
from drag_constant_Cdo import drag_constant_Cdo
from fuel_weight_ratio_estimate import fuel_weight_ratio_estimate
from ambiance import Atmosphere
import numpy as np

def calc_landing_FL_W_S(W_S,  M_cruise, sweep, AR, density, alt, Cdo, LNDFL):
    CL_max_LND = Mdd_constraint(W_S, M_cruise, alt, sweep, AR)[1]

    ##Descent
    CL = CL_max_LND / (1.3**2)
    L_D_descent = CL / drag_constant_Cdo(CL, AR, True, 'LND',0, M_cruise, Cdo)
    h_obs = 50 #obstance height
    c1 = LNDFL * 0.6 - L_D_descent * h_obs
    c2 = 0.3675 * L_D_descent / (density * 32.2 * CL_max_LND)

    ##Gnd roll
    CL_lnd_gnd_roll = 0.1
    Cd_lnd_roll = drag_constant_Cdo(CL_lnd_gnd_roll, AR, True, 'LND', 0, M_cruise, Cdo)
    mu = 0.22 #Friction coefficent
    c3 = 1/ (density * 32.2 * (mu * CL_lnd_gnd_roll - Cd_lnd_roll))
    c4 = -mu * CL_max_LND / (mu * CL_max_LND + 1.3225 * (mu*CL_lnd_gnd_roll - Cd_lnd_roll))

    W_S_LND = c1 / (c2 + c3 * np.log(c4))
    W_S_TO = W_S_LND / (1-(1-0.45) *  fuel_weight_ratio_estimate(7000, M_cruise, alt))
    return W_S_TO

def iterate_W_S_LND(W_S,  M_cruise, sweep, AR, alt, Cdo, LNDFL, temp_delta):
    densityHot = Atmosphere(0).pressure[0] / 287 / (Atmosphere(0).temperature[0] + temp_delta) * 0.00194032  # convert to lbf/ft^3
    W_S_new = calc_landing_FL_W_S(W_S, M_cruise, sweep, AR, densityHot, alt, Cdo, LNDFL)

    while(np.abs(W_S_new - W_S) > 0.0001):
        W_S = W_S_new
        W_S_new = calc_landing_FL_W_S(W_S, M_cruise, sweep, AR, densityHot, alt, Cdo, LNDFL)

    return W_S







