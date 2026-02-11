import numpy as np
from drag_constant_Cdo import drag_constant_Cdo
from ambiance import Atmosphere
from Propulsion import propulsion


def service_ceiling(W_S, h_ceiling, h_cruise=35000, AR = 10, M_cruise = 0.85, ROC=100):
    Cd, L_D, Cdo, e = drag_constant_Cdo(1, 1, AR, False, False, 0, 0.85)  #inputs CL, CL max, M not needed
    rho_ceiling = Atmosphere(h_ceiling * 0.3048).density[0] * 0.00194032
    K = 1 / (e * AR * np.pi)
    CL_best_L_D = np.sqrt(Cdo / K)
    V_best_L_D = np.sqrt(2 * W_S * 0.965 / rho_ceiling / CL_best_L_D)
    thrust_max, lapse = propulsion(h_ceiling, M_cruise)

    T_W_guess = 0.4
    T_W_climb = T_W_guess * lapse
    eta = T_W_climb * np.sqrt(1 / (Cdo * K))

    V_ratio = np.sqrt( (eta + np.sqrt(eta ** 2 + 12)) / 6) #ratio Vy to V_best_L_D
    Vy = V_best_L_D * V_ratio
    CLy = CL_best_L_D / V_ratio ** 2
    a_ceiling = (Atmosphere(h_ceiling * 0.3048).speed_of_sound[0] * 3.28084)
    My = Vy / a_ceiling

    V_cruise = M_cruise * Atmosphere(h_cruise * 0.3048).speed_of_sound[0] * 3.28084
    rho_cruise = Atmosphere(h_cruise * 0.3048).density[0] * 0.00194032
    CL_cruise = 2 * W_S / (rho_cruise * V_cruise ** 2)

    Mdiv_cruise = M_cruise + 0.004
    delta_Mdiv = np.polyval([0.84225806, -1.77681462, 1.03674548, -0.17259473], CL_cruise)
    Mdiv_CL_55 = Mdiv_cruise - delta_Mdiv  # Solves for Mdiv at CL = .55
    delta_Mdiv_CL_y = np.polyval([ 0.84225806, -1.77681462,  1.03674548, -0.17259473], CLy)
    Mddy = Mdiv_CL_55 - delta_Mdiv_CL_y

    while Mddy < My + 0.004:
        My = Mddy - 0.004
        Vy = My * a_ceiling
        CLy = 2 * W_S * 0.965 / (rho_ceiling * Vy **2)
        delta_Mdiv_CL_y = np.polyval([0.84225806, -1.77681462, 1.03674548, -0.17259473], CLy)
        Mddy = Mdiv_CL_55 - delta_Mdiv_CL_y

    L_D_climb = drag_constant_Cdo(CLy, 3, AR, False, False, My, Mddy)[1] #CL max not needed because in cruise config
    T_W_climb = 1 / L_D_climb + (ROC/60) / Vy
    lapse_climb = propulsion(h_ceiling, My)[1]
    T_W = T_W_climb * 0.965/lapse_climb

    return T_W

#print(service_ceiling(100, 40000, 35000, 10, 0.85))

