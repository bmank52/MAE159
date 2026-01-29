from fuel_weight_ratio_estimate import fuel_weight_ratio_estimate
from Mdd_constraint import Mdd_constraint
import numpy as np
from ambiance import Atmosphere
from Propulsion import propulsion

def takeoff_field_length(W_S, sweep, AR, n_eng=2, M_cruise=0.85, alt=35000, range=7000, TOFL=9000, temp_delta=22.8):
    Mdd = Mdd_constraint(W_S, M_cruise, alt, sweep, AR)
    t2c = Mdd[0]
    CL_max_TO =  Mdd[2]
    CL_max_LND = Mdd[1]
    CL_max_clean = Mdd[3]
    Wf_WTO = fuel_weight_ratio_estimate(range, M_cruise, alt)

    TOFL = TOFL / 1000 #Fig 5 requires TOFLe-3

    if n_eng == 2:
        TOP = np.polyval([ 2.13223427e-02, -7.57281792e-01,  3.61062294e+01, -2.91080694e+01], TOFL)
    elif n_eng ==3:
        TOP = np.polyval([ 3.32098747e-02, -1.03395661e+00,  4.11258055e+01, -3.03777606e+01], TOFL)
    elif n_eng == 4:
        TOP = np.polyval([ 3.02525553e-02, -9.95769835e-01,  4.19866315e+01, -2.06661439e+01], TOFL)

    rho_hot = Atmosphere(0).pressure[0] / 287 / (Atmosphere(0).temperature[0] + temp_delta) * 0.00194032
    V_LO = 1.2 * np.sqrt(2 * W_S / (rho_hot * CL_max_TO))
    sigma = rho_hot / (Atmosphere(0).density[0] * 0.00194032)
    T2W_70V_Lo = W_S / (TOP * sigma * CL_max_TO)

    T_TO = (Atmosphere(0).temperature[0] + 22.8) * 1.8 #Kelvin to rankine
    a_TO = np.sqrt(1.4 * 1718 * T_TO)
    Ma_TO = V_LO * .7 / a_TO

    lapse = propulsion(0, Ma_TO)[1]
    T2W = T2W_70V_Lo / lapse

    return T2W


print(takeoff_field_length(130, 35, 10))