import numpy as np

def drag_constant_Cdo(CL, CL_max, AR, gear_down, flaps, M, M_cruise, Cdo=0.015):    #input CL, AR, t/f, TO/LND/f, M, M_cruise, Cdo
    e = 1 / (1.035 + .38 * Cdo * np.pi *AR)
    Cd = Cdo + CL ** 2 / (np.pi * e * AR)
    CL_ratio = CL / CL_max

    if gear_down:
        Cd += Cdo

    if M == M_cruise:
        Cd += 0.001

    if not flaps:   # no flaps, if false
        return [Cd, CL / Cd, Cdo, e]
    elif flaps =="TO":   #flaps in Take off config
        Cd += np.polyval([ 0.11488358, -0.04715969, -0.04596621,  0.03125494], CL_ratio)
        return [Cd, CL/Cd, Cdo, e]
    else:                 #flaps in landing config
        Cd += np.polyval([ 0.08532904,  0.00289963, -0.06521609,  0.04009689], CL_ratio)
        return [Cd, CL / Cd, Cdo, e]

