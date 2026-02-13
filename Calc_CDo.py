import numpy as np
from ambiance import Atmosphere
from scipy.constants import atm


#Given inputs calculates Cdo
def calc_CD0(h, M, l_f, d_f, Sref, mac, sweep, t2c, T_SLSD):
    atm = Atmosphere(h * 0.3048)
    V = M * atm.speed_of_sound[0] * 3.28084 #velocity
    rho = atm.density[0] * 0.00194032 #density in slugs/ft3
    mu = atm.dynamic_viscosity[0] * 0.0208854 #Pa s to lb s /ft2
    unit_Re = V * rho / mu

    #fuselage
    Re_fuselage = unit_Re * l_f
    friction_coeff = np.poly1d([ 0.01572842, -0.41540515,  2.65902818])
    log_Re_fuselage = np.log10(Re_fuselage)
    log_Cf_fuselage = friction_coeff(log_Re_fuselage)
    Cf_fuselage = 10 ** log_Cf_fuselage / 1000
    Swet_f = 0.9 * np.pi * d_f * l_f
    fineness_f = l_f / d_f
    K_f = np.polyval([-1.68590746e-03,  4.32149329e-02, -3.92899783e-01,  2.37900023e+00], fineness_f)
    f_fuselage = K_f * Cf_fuselage * Swet_f

    #wing
    Re_wing = unit_Re * mac
    friction_coeff = np.poly1d([0.01572842, -0.41540515, 2.65902818])
    log_Re_wing = np.log10(Re_wing)
    log_Cf_wing = friction_coeff(log_Re_wing)
    Cf_wing = 10 ** log_Cf_wing / 1000
    Swet_wing = 2 * 1.02 * (Sref - d_f * mac)
    M0 = 0.5
    Z = (2 - M0 **2) * np.cos(np.radians(sweep)) / np.sqrt(1 - M0 ** 2 * np.cos(np.radians(sweep)) ** 2)
    fineness_wing = 1 + Z * t2c + 100 * t2c ** 4
    K_wing = np.polyval([-1.68590746e-03, 4.32149329e-02, -3.92899783e-01, 2.37900023e+00], fineness_wing)
    f_wing = K_wing * Cf_wing * Swet_wing

    f_tail = 0.25 * f_wing
    Cf_nacelle = Cf_wing
    n_eng = 2
    Swet_nacelle = 2.1 * n_eng * np.sqrt(T_SLSD)
    K_nacelle = 1.25

    f_nacelle = K_nacelle * Swet_nacelle * Cf_nacelle
    f_pylon = 0.2 * f_nacelle
    Cdo = 1.06 * (f_fuselage + f_wing + f_tail + f_nacelle + f_pylon)/Sref

    '''
    # DEBUG PRINT FOR CD0 COMPONENTS
    print(f"\n--- CD0 Debug (h={h}ft, M={M}) ---")
    print(f"Component Drag Areas (f = K * Cf * Swet):")
    print(f"  Fuselage: {f_fuselage:.4f}")
    print(f"  Wing:     {f_wing:.4f}")
    print(f"  Tail:     {f_tail:.4f}")
    print(f"  Nacelle:  {f_nacelle:.4f}")
    print(f"  Pylon:    {f_pylon:.4f}")
    print(f"Total Cdo:  {Cdo:.6f}")
    print(f"-----------------------------------\n")
    '''

    return Cdo

