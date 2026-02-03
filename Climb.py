import numpy as np
from fuel_weight_ratio_estimate import fuel_weight_ratio_estimate
from Mdd_constraint import Mdd_constraint
from ambiance import Atmosphere
from drag_constant_Cdo import drag_constant_Cdo
from Propulsion import propulsion

### Part 25 Climb Requirements ###
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
### JT9D Engine Line Coefficents %%%
SL_Dry_TO = [ -2.32298858,  38.88677337, -47.75554851,  45.36765101] #Ask about Hot day vs normal day
Max_Climb_SL = [ 22.13898722, -54.46971846,  58.66542734, -46.08558042,  38.16264537]
Max_Climb_15k = [ 18.54452785, -45.40374196,  44.78269334, -29.19659026,  27.17125099]

def climb_gradient(W_S, segment, range=7000, AR = 10, Sweep = 35, M_cruise = 0.85, cruise_alt=35000):
    alt = segment["alt"]
    if segment["Weight"] == "MTOW":
        W_W_TO = 1
        W_S = W_S * W_W_TO
    else:
        Wf_W = fuel_weight_ratio_estimate(range, M_cruise, cruise_alt)
        Wf_LND_W_TO = 0.45
        W_W_TO = 1 - Wf_W + Wf_LND_W_TO * Wf_W
        W_S = W_S * W_W_TO #landing wing loading based on fuel burn

    t2c, CL_max_LND, CL_max_TO, CL_max_clean = Mdd_constraint(W_S, M_cruise, alt, Sweep, AR)
    if segment["Flaps"] == "LND":
        CL_max = CL_max_LND
    elif segment["Flaps"] == "TO":
        CL_max = CL_max_TO
    else:
        CL_max = CL_max_clean

    temp_delta = 22.8 #K
    R = 287 # J / kg K
    T = Atmosphere(alt).temperature[0] + temp_delta # Kelvin
    rho_hot = Atmosphere(alt).pressure[0] / R / T * 0.00194032
    Vstall = np.sqrt(2 * W_S / rho_hot / CL_max)
    V_Vstall = segment["V_Vstall"]
    CL = CL_max / (V_Vstall) ** 2
    M = (Vstall * V_Vstall) / np.sqrt(1.4 * R * T ) / 3.28084
    L_D = drag_constant_Cdo(CL, CL_max, AR,segment["Gear"], segment["Flaps"], M, M_cruise)[1]


    T_W_climb = 1 / L_D + segment["climb_gradient_2_eng"] / 100
    n_eng = 2
    if segment["OEI"]:
        n_eng_ratio = n_eng / (n_eng - 1) #total vs opperative eng
    else:
        n_eng_ratio = 1

    lapse = propulsion(alt, M)[1]

    T_W = T_W_climb * W_W_TO / lapse * n_eng_ratio
    return T_W



