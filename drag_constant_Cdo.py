import numpy as np

def drag_constant_Cdo(CL, CL_max, AR, gear_down, flaps, M, M_cruise, Cdo):    #input CL, AR, t/f, TO/LND/f, M, M_cruise, Cdo
    e = 1 / (1.035 + .38 * Cdo * np.pi *AR)
    Cd = Cdo + CL ** 2 / (np.pi * e * AR)
    CL_ratio = CL / CL_max

    if gear_down:
        Cd += Cdo

    if M == M_cruise:
        Cd += 0.001

    if not flaps:   # no flaps, if false
        return Cd
    elif flaps =="TO":   #flaps in Take off config
        return Cd += np.polyval([ 76.30335562, -61.95312041, 16.6308463, 1.04415875], CL_ratio)
    else:                 #flaps in landing config
        return Cd += np.polyval([108.18261739,-67.42614684,16.39380699,1.99475706], CL_ratio)


