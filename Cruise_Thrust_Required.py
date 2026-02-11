from ambiance import Atmosphere
from drag_constant_Cdo import drag_constant_Cdo
from Propulsion import propulsion

def Cruise_Thrust_Required(W_S, AR, M_cruise = 0.85, h = 35000):
    V_cruise = M_cruise * Atmosphere(h * 0.3048).speed_of_sound[0] * 3.28084  #Converts h to m for atmosphere, converts m/s  to fps
    rho_cruise = Atmosphere(h * 0.3048).density[0] * 0.00194032 #Converts kg/m3 to slug/ft3
    W_S_Cruise_Start = 0.965 * W_S
    CL = 2 * W_S_Cruise_Start / (rho_cruise * V_cruise ** 2)
    L_D = drag_constant_Cdo(CL, CL, AR, False, False, M_cruise, M_cruise)[1]
    lapse = propulsion(h, M_cruise)[1]

    T_W = 0.965 / L_D / lapse
    return T_W


#print(Cruise_Thrust_Required(100, 10, 0.85))
