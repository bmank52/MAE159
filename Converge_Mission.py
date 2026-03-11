import numpy as np

from fuel_weight_ratio_estimate import fuel_weight_ratio_estimate
from Mdd_constraint import Mdd_constraint
from Converge_TO_weight import converge_TO_weight
from Resize_Geometry import resize_geometry
from Resize_Engine import resize_engine
from Fly_Mission import fly_mission


def converge_fuel_ratio(Wf_Wto, W_S, T_W, AR, taper, t2c, sweep, pax, payload, alt, range, M_cruise):
    W_TO = converge_TO_weight(Wf_Wto, W_S, T_W, AR, taper, t2c, sweep, pax, payload)
    S_ref, mac, b_ref, Cr, Ct, mac_quarter_c, L_f, D_f  = resize_geometry(W_TO, W_S, AR, sweep, taper, pax)
    T_SLSD_SE, eng_scaling = resize_engine(W_TO, T_W)
    Wf_Wto_new = fly_mission(W_TO, alt, AR, S_ref, T_W, L_f, D_f, mac, sweep, t2c, Wf_Wto, T_SLSD_SE, range, M_cruise)

    alpha = .5 #for under relaxation
    while np.abs(Wf_Wto_new - Wf_Wto) > .01:
        Wf_Wto = alpha * Wf_Wto_new + (1-alpha) * Wf_Wto
        W_TO = converge_TO_weight(Wf_Wto, W_S, T_W, AR, taper, t2c, sweep, pax, payload)
        S_ref, mac, b_ref, Cr, Ct, mac_quarter_c, L_f, D_f = resize_geometry(W_TO, W_S, AR, sweep, taper, pax)
        T_SLSD_SE, eng_scaling = resize_engine(W_TO, T_W)
        Wf_Wto_new = fly_mission(W_TO, alt, AR, S_ref, T_W, L_f, D_f, mac, sweep, t2c, Wf_Wto, T_SLSD_SE, range,M_cruise)

    return Wf_Wto_new

def converge_mission(W_S, T_W, sweep, AR, range, M_cruise, alt, taper, payload, pax):
    Wf_Wto = fuel_weight_ratio_estimate(range, M_cruise, alt) #guess fuel ratio estimate
    t2c, CL_max_LND, CL_max_TO, CL_max_clean = Mdd_constraint(W_S, M_cruise, alt, sweep, AR)
    W_TO = converge_TO_weight(Wf_Wto, W_S, T_W, AR, taper, t2c, sweep, pax, payload)
    Wf_Wto = converge_fuel_ratio(Wf_Wto, W_S, T_W, AR, taper, t2c, sweep, pax, payload, alt, range, M_cruise)
    return W_TO, Wf_Wto



def create_TW_WS_grid(N_WS, N_TW, lower_WS, upper_WS, lower_TW, upper_TW, sweep, AR, range, M_cruise, alt, taper, payload, pax):
    WS_range = np.linspace(lower_WS, upper_WS, N_WS) #create range of W/S
    TW_range = np.linspace(lower_TW, upper_TW, N_TW) #Create range of T/W

    W_TO_grid = np.zeros([N_WS, N_TW]) #2D array to store W_TO for W/S and T/W
    for i, WS in enumerate(WS_range):
        for j, TW in enumerate(TW_range):
            W_TO = converge_mission(WS, TW, sweep, AR, range, M_cruise, alt, taper, payload, pax)[0]
            print(W_TO)
            W_TO_grid[i, j] = W_TO

    return WS_range, TW_range, W_TO_grid




print(converge_mission(90, .3, 30, 8, 3000, .82, 35000, .35, 10000, 150))

