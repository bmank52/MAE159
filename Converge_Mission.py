from fuel_weight_ratio_estimate import fuel_weight_ratio_estimate
from Mdd_constraint import Mdd_constraint
from Converge_TO_weight import converge_TO_weight
from Resize_Geometry import resize_geometry
from Resize_Engine import resize_engine

def converge_fuel_ratio(Wf_Wto, W_S, T_W, AR, taper, t2c, sweep, pax, payload):
    W_TO = converge_TO_weight(Wf_Wto, W_S, T_W, AR, taper, t2c, sweep, pax, payload)
    S_ref, mac, b_ref, Cr, Ct, mac_quarter_c = resize_geometry(W_TO, W_S, AR, sweep, taper)
    T_SLSD_SE, eng_scaling = resize_engine(W_TO, T_W)
    


def converge_mission(W_S, T_W, sweep, AR, range=7000, M_cruise=0.85, alt=35000, taper=.35, payload=12000, pax=250):
    Wf_Wto = fuel_weight_ratio_estimate(range, M_cruise, alt) #guess fuel ratio estimate
    t2c, CL_max_LND, CL_max_TO, CL_max_clean = Mdd_constraint(W_S, M_cruise, alt, sweep, AR)
    W_TO = converge_TO_weight(Wf_Wto, W_S, T_W, AR, taper, t2c, sweep, pax, payload)




