from ambiance import Atmosphere
import numpy as np
from numpy.polynomial.polynomial import polyval

###Takes inputs W/S, M cruise, altitude, sweep, AR and outputs t2c, CL max clean/LND/TO

def Mdd_constraint(W_S, M_cruise, alt, sweep, AR):  #inputs wing loading, cruise mach, altitude, sweep, aspect ratio
    V_cruise = M_cruise * Atmosphere(alt * 0.3048).speed_of_sound[0] * 3.28 # Converts M to ft/s
    W_S_start_cruise = 0.965 * W_S # Wing Loading at the start of cruise based on wing loading at TO (lb/ft^2)
    CL_start_cruise = 2 * W_S_start_cruise / (Atmosphere(alt * 0.3048).density[0] * 0.00194032 * V_cruise ** 2)  # Solves for CL, coverts density to slug/ft^3
    Mdiv_cruise = M_cruise + 0.004
    delta_Mdiv = np.polyval([ 0.84225806, -1.77681462,  1.03674548, -0.17259473], CL_start_cruise)
    Mdiv_CL_55 = Mdiv_cruise - delta_Mdiv #Solves for Mdiv at CL = .55

    ###evaluate t/c based on Mdiv and sweep###
    #define all the coeffcients for the curve fit polynomials in a dictionary call coeff
    coeff_fig1b = {
        0: [-39.7549175,   92.41214705, -72.28355364,  19.10814267],
        5: [-31.11146289,  73.48954762, - 58.51214756,  15.77914856],
        10: [-21.31031118,  51.90339771, - 42.70680097,  11.93831232],
        15: [-23.5652596,   57.58056877, - 47.46507883,  13.27498474],
        20: [-16.23553185,  41.22504864, - 35.40033157,  10.34869903],
        25: [-20.17360599,  51.758047, - 44.79349569,  13.15206791],
        30: [-18.08048569,  48.41512699, -43.73554189,  13.39546818],
        35: [ -42.27563259,  112.74413074, -100.96943293,   30.44700561],
        40: [ -450.35907195,  1184.0633946,  -1039.38030036,   304.74912947]
    }

    if sweep <= 5:   #sweep from 0 to 5
        sweep0 = np.polyval(coeff_fig1b[0], Mdiv_CL_55)
        sweep5 = np.polyval(coeff_fig1b[5], Mdiv_CL_55)
        t2c = np.interp(sweep, [0, 5], [sweep0, sweep5])   #based on surrounding sweep data, extrapolate to find desired sweep t/c
    elif sweep <= 10:   #5-10
        sweep5 = np.polyval(coeff_fig1b[5], Mdiv_CL_55)
        sweep10 = np.polyval(coeff_fig1b[10], Mdiv_CL_55)
        t2c = np.interp(sweep, [5, 10], [sweep5, sweep10])
    elif sweep <= 15: #10-15
        sweep10 = np.polyval(coeff_fig1b[10], Mdiv_CL_55)
        sweep15 = np.polyval(coeff_fig1b[15], Mdiv_CL_55)
        t2c = np.interp(sweep, [10, 15], [sweep10, sweep15])
    elif sweep <= 20: #15-20
        sweep15 = np.polyval(coeff_fig1b[15], Mdiv_CL_55)
        sweep20 = np.polyval(coeff_fig1b[20], Mdiv_CL_55)
        t2c = np.interp(sweep, [15, 20], [sweep15, sweep20])
    elif sweep <= 25: #20-25
        sweep20 = np.polyval(coeff_fig1b[20], Mdiv_CL_55)
        sweep25 = np.polyval(coeff_fig1b[25], Mdiv_CL_55)
        t2c = np.interp(sweep, [20, 25], [sweep20, sweep25])
    elif sweep <= 30: #25-30
        sweep25 = np.polyval(coeff_fig1b[25], Mdiv_CL_55)
        sweep30 = np.polyval(coeff_fig1b[30], Mdiv_CL_55)
        t2c = np.interp(sweep, [25, 30], [sweep25, sweep30])
    elif sweep <= 35: #30-35
        sweep30 = np.polyval(coeff_fig1b[30], Mdiv_CL_55)
        sweep35 = np.polyval(coeff_fig1b[35], Mdiv_CL_55)
        t2c = np.interp(sweep, [30, 35], [sweep30, sweep35])
    else: #35-40   not sure best way to handle case above 40 deg, currently max at 35 deg due to limitation in fig 3b
        sweep35 = np.polyval(coeff_fig1b[35], Mdiv_CL_55)
        sweep40 = np.polyval(coeff_fig1b[40], Mdiv_CL_55)
        t2c = np.interp(sweep, [35, 40], [sweep35, sweep40])


    ###Calculate CL max TO and Lnd ###
    coeff_CL_max_landing = [108.18261739, -67.42614684,  16.39380699,   1.99475706]  #fig 3
    coeff_CL_max_TO = [ 76.30335562, -61.95312041,  16.6308463,    1.04415875] # fig 3
    x = (np.cos(np.deg2rad(sweep)) * t2c) ** 2 * AR
    CL_max_LND = np.polyval(coeff_CL_max_landing, x)   #output
    CL_max_TO = np.polyval(coeff_CL_max_TO, x)  #output


    ###Calculate CL max clean using fig 3b###
    coeff_fig3b = {
        0: [-321.26954473,   83.11933347,   -2.46418685,    0.94522571],
        15: [-337.36190906,   88.66983361,   -2.93791529,    0.90236749],
        35: [-323.19372374,   84.86130085,   -2.69609881,    0.85002387]
    }

    if sweep <=15:
        sweep0 = np.polyval(coeff_fig3b[0], t2c)
        sweep15 = np.polyval(coeff_fig3b[15], t2c)
        CL_max_clean = np.interp(sweep, [0, 15], [sweep0, sweep15])
    elif sweep <= 35:
        sweep15 = np.polyval(coeff_fig3b[15], t2c)
        sweep35 = np.polyval(coeff_fig3b[35], t2c)
        CL_max_clean = np.interp(sweep, [15, 35], [sweep15, sweep35])
    else:
        CL_max_clean = np.polyval(coeff_fig3b[35], t2c) #Not sure best way to handle his case, for now max out at 35 deg sweep

    return [t2c, CL_max_LND, CL_max_TO, CL_max_clean]

print(Mdd_constraint(44.24, 0.8, 35000, 35, 10))