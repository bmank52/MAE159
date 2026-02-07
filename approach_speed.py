import numpy as np
from Mdd_constraint import Mdd_constraint
from fuel_weight_ratio_estimate import fuel_weight_ratio_estimate
from ambiance import Atmosphere

def calc_W_S_new(W_S, M_cruise, sweep, AR, Vapp, range, density, alt, max_LND_fuel_weight_ratio): #input temp_delta for degrees C different than standard
    CL_max_Lnd = Mdd_constraint(W_S, M_cruise, alt, sweep, AR)[1]
    W_S_Lnd = 0.5 * density * CL_max_Lnd * (Vapp/1.3) ** 2
    W_S = W_S_Lnd * 1 / (1-(1-max_LND_fuel_weight_ratio) * fuel_weight_ratio_estimate(range, M_cruise, alt))

    return W_S

def iterate_W_S_approach(W_S, M_cruise, sweep, AR, Vapp, range, temp_delta=22.6, alt=35000, max_LND_fuel_weight_ratio=0.45): #input Vap in kts, temp_delta for degrees C different than standard
    Vapp = Vapp * 1.68781 #converts to ft/s
    atm = Atmosphere(0)
    rho_std = atm.density[0]
    temp_std = atm.temperature[0]
    temp_hot = temp_std + temp_delta


    densityHot = rho_std * temp_std / temp_hot * 0.00194032  # convert to lbf/ft^3
    W_S_new = calc_W_S_new(W_S, M_cruise, sweep, AR, Vapp, range, densityHot, alt, max_LND_fuel_weight_ratio)
    while(np.abs(W_S_new - W_S) > 0.01):
        W_S = W_S_new
        W_S_new = calc_W_S_new(W_S, M_cruise, sweep, AR, Vapp, range, densityHot, alt, max_LND_fuel_weight_ratio)
    return W_S_new


#print(iterate_W_S_approach(130, 0.82, 35, 10, 130, 3000, 22.6, 35000, 0.4))

