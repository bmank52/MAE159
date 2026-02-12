from fuel_weight_ratio_estimate import fuel_weight_ratio_estimate
from Mdd_constraint import Mdd_constraint


def converge_mission(W_S, T_W, sweep, AR, range=7000, M_cruise=0.85, alt=35000):
    Wf_Wto = fuel_weight_ratio_estimate(range, M_cruise, alt) #guess fuel ratio estimate
    t2c, CL_max_LND, CL_max_TO, CL_max_clean = Mdd_constraint(W_S, M_cruise, alt, sweep, AR)


