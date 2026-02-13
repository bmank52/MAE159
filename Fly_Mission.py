import numpy as np
from drag_constant_Cdo import drag_constant_Cdo
from Propulsion import propulsion
from Resize_Engine import resize_engine
from ambiance import Atmosphere
from Calc_CDo import calc_CD0
from Propulsion import TSFC_at_alt


def fly_climb(W_TO, h_cruise, AR, Sref, T_W, L_f, D_f, mac, sweep, t2c, M_cruise=.85):
    W0 = W_TO #starting guess
    W1 = 0.965 * W0 #weight at end of climb
    W_climb = (W0 + W1) / 2 #Climb weight estimate
    h_climb = h_cruise / 2 #Climb alt estimate
    atm = Atmosphere(h_climb * 0.3048) #get atm values at h_climb in SI units
    rho_climb = atm.density[0] * 0.00194032 #density in slug/ft3
    Cd, L_D, Cdo, e = drag_constant_Cdo(1, 3, AR, False, False, .5, M_cruise) #Arbitary CL and Machs, only need Cdo, e
    k = 1 / (np.pi * AR * e) #calc K from e and AR

    W_S_climb = W_climb / Sref #Climb wing loading
    M_climb = M_cruise #guess
    n_eng = 2 #From RFP
    eng_scaling = resize_engine(W_climb, T_W)[1] #Engine scaling vs JT9D
    T_SLSD_JT9D = 45500
    T_SLSD = T_SLSD_JT9D * eng_scaling

    T_max_climb = float(propulsion(h_climb, M_climb)[0]) #max thrust of JT9D
    T_W_climb = (T_max_climb * n_eng * eng_scaling) / W_climb
    Vy = np.sqrt(W_S_climb / (3 * rho_climb * Cdo) * (T_W_climb + np.sqrt(T_W_climb ** 2 + 12 * Cdo * k))) #calc climb velocity
    #Assume L=W
    CL = 2 * W_S_climb / (rho_climb * Vy ** 2) #Calc lift coefficent

    Cdo = calc_CD0(h_climb, M_climb, L_f, D_f, Sref, mac, sweep, t2c, T_SLSD) #calc new Cdo
    a_climb = atm.speed_of_sound[0] * 3.28084 #speed of sound in ft/2
    M_climb = Vy / a_climb #Mach number in climb
    Cd, L_D, Cdo, e = drag_constant_Cdo(CL, 3, AR, False , False, M_climb, M_cruise, Cdo) #get drag values
    Drag_climb = .5 * rho_climb * Vy**2 * Cd * Sref #drag in climb

    T_avail_climb = float(propulsion(h_climb, M_climb)[0]) * n_eng * eng_scaling #
    T_per_engine_unscaled = T_avail_climb / (n_eng * eng_scaling)
    h_climb = 15000 #force to check at 15k
    TSFC = TSFC_at_alt(M_climb, T_per_engine_unscaled, h_climb)
    TSFC = float(np.asarray(TSFC).flatten()[0]) / 3600

    W1_W0 = np.exp(-TSFC*h_cruise/(Vy * (1-Drag_climb/T_avail_climb)))
    RoC = (T_avail_climb - Drag_climb) / W_climb * Vy
    delta_time = h_cruise / RoC
    range_climb = delta_time * Vy #ft
    return W1_W0, range_climb







def fly_cruise(W_TO, Wf_Wto, T_W, Sref, AR, L_f, D_f, mac, sweep, t2c, T_SLSD, range=7000,  M_cruise=.85, h_cruise=35000):
    atm = Atmosphere(h_cruise * 0.3048)
    Wo = W_TO * .965 #guess weight at cruise start
    W1 = (1 - Wf_Wto) * W_TO #guess weight at end of cruise
    W_cruise = (Wo + W1) / 2 #average cruise weight

    W_S_cruise = W_cruise / Sref #average  cruise wing loading
    a_cruise = atm.speed_of_sound[0] * 3.28084  #speed of sound ft/s
    V_cruise = M_cruise * a_cruise  #ft/s

    #L=W
    rho_cruise = atm.density[0] * 0.00194032 #density in slug/ft3
    CL = 2*W_S_cruise / (rho_cruise * V_cruise ** 2)

    Cdo = calc_CD0(h_cruise, M_cruise, L_f, D_f, Sref, mac, sweep, t2c, T_SLSD)  # calc new Cdo
    Cd, L_D, Cdo, e = drag_constant_Cdo(CL, 3, AR, False, False, M_cruise, M_cruise, Cdo)  # get drag values

    #T=D
    n_eng = 2
    Thrust_cruise = Cd * .5 * rho_cruise * V_cruise ** 2 * Sref #T=D
    eng_scaling = resize_engine(W_cruise, T_W, n_eng)[1]
    Thrust_avail_cruise = float(propulsion(h_cruise, M_cruise)[0]) * n_eng * eng_scaling

    if Thrust_cruise > Thrust_avail_cruise: #error check to keep code from crashing
        Thrust_cruise = Thrust_avail_cruise

    T_per_engine_unscaled = Thrust_cruise / (n_eng * eng_scaling)
    TSFC = TSFC_at_alt(M_cruise, T_per_engine_unscaled, h_cruise) #get specific fuel consumption
    TSFC = float(np.asarray(TSFC).flatten()[0])


    V_kts = V_cruise * 0.592484 #cruise velocity in kts
    Range_All_out =  range + 200 + .75 * V_kts # Mission range + 200 nmi + 45mins cruise speed KNOTS
    R_climb = fly_climb(W_TO, h_cruise, AR, Sref, T_W, L_f, D_f, mac, sweep, t2c, M_cruise)[1] #ft
    R_climb_kts = R_climb * 0.000164579 #climb range in kts

    R_cruise = Range_All_out - R_climb_kts #cruise range in kts
    W1_W0_cruise = np.exp(- R_cruise * TSFC / (V_kts * L_D)) #Breguet eqn to fuel ratio
    return W1_W0_cruise

def fly_mission(W_TO, h_cruise, AR, Sref, T_W, L_f, D_f, mac, sweep, t2c, Wf_Wto, T_SLSD, range=7000, M_cruise=0.85):
    W1_W0_climb = fly_climb(W_TO, h_cruise, AR, Sref, T_W, L_f, D_f, mac, sweep, t2c, M_cruise)[0]
    W2_W1_cruise = fly_cruise(W_TO, Wf_Wto, T_W, Sref, AR, L_f, D_f, mac, sweep, t2c, T_SLSD, range, M_cruise, h_cruise)
    Wf_Wto = 1 - W1_W0_climb * W2_W1_cruise
    return Wf_Wto




W_TO_test = 350000      # Takeoff Weight (lbs)
h_cruise_test = 35000   # Cruise Altitude (ft)
AR_test = 9.0           # Aspect Ratio
Sref_test = 3000        # Wing Reference Area (sq ft)
T_W_test = 0.28         # Thrust-to-Weight Ratio
L_f_test = 180          # Fuselage Length (ft)
D_f_test = 18           # Fuselage Diameter (ft)
mac_test = 16           # Mean Aerodynamic Chord (ft)
sweep_test = 31.5       # Wing Sweep (degrees)
t2c_test = 0.12         # Thickness-to-chord ratio
Wf_Wto_guess = 0.3      # Initial Fuel Fraction guess (30%)
T_SLSD_test = 50000     # Sea Level Static Thrust per engine (lbs)
range_nm_test = 4000    # Mission Range (nmi)
M_cruise_test = 0.80    # Cruise Mach
# --- Full Mission Test ---
print("\n--- Starting Full Mission Test ---")
try:
    Wf_Wto_final = fly_mission(
        W_TO_test, h_cruise_test, AR_test, Sref_test, T_W_test,
        L_f_test, D_f_test, mac_test, sweep_test, t2c_test,
        Wf_Wto_guess, T_SLSD_test, range_nm_test, M_cruise_test
    )
    print(f"Success! Final Fuel Fraction: {Wf_Wto_final:.4f}")

except Exception as e:
    import traceback

    print("Full Mission failed. Details:")
    traceback.print_exc()