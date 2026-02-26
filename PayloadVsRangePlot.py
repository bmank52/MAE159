from Fly_Mission import fly_climb
from Fly_Mission import fly_cruise
from ambiance import Atmosphere
from Calc_CDo import calc_CD0
from drag_constant_Cdo import drag_constant_Cdo
from Resize_Engine import resize_engine
from Propulsion import TSFC_at_alt
import numpy as np
import matplotlib.pyplot as plt

# --- Aircraft Constants ---
WTO_design = 390000
WF_WTO_design = 0.45
h_cruise = 35000
M_cruise = 0.85
atm = Atmosphere(h_cruise * 0.3048)
AR = 8
Sref = 2900
T_W = .3
L_f = 190
D_f = 15
mac = 12
sweep = 40
t2c = .18
n_eng = 2

# Engine and Drag setup
Thrust_1_JT9D, eng_scaling = resize_engine(WTO_design, T_W, n_eng)
T_SLSD = 61018.08
Cd0 = calc_CD0(h_cruise, M_cruise, L_f, D_f, Sref, mac, sweep, t2c, T_SLSD)

# Payload definitions
maxPayload = 90000  # Structural Limit
designPax = 250
paxWeight = 250
designCargo = 12000
designPayload = designPax * paxWeight + designCargo  # 74,500 lbs

# Weight Breakdown
Wf_max = WF_WTO_design * WTO_design  # Assuming design fuel is the tank capacity
OEW = WTO_design - designPayload - Wf_max


def calcPayloadRange(W_TO, Wf_Wto, Cd0):
    # Ensure Wf_Wto never exceeds physical limits or creates negative weights
    Wf_Wto = max(0, min(Wf_Wto, 0.99))

    W1_W0, climbRange = fly_climb(W_TO, h_cruise, AR, Sref, T_W, L_f, D_f, mac, sweep, t2c, M_cruise)
    W0 = W_TO * W1_W0
    W1 = (1 - Wf_Wto) * W_TO

    # Simple check to prevent log of negative/zero
    if W0 <= W1: return 0

    W_Cruise = (W0 + W1) / 2
    V_cruise = M_cruise * atm.speed_of_sound[0] * 3.28084
    rho_cruise = atm.density[0] * 0.00194032
    CL = 2 * (W_Cruise / Sref) / (rho_cruise * V_cruise ** 2)

    Cd, L_D, _, _ = drag_constant_Cdo(CL, 3, AR, False, False, M_cruise, M_cruise, Cd0)
    Thrust = Cd * 0.5 * rho_cruise * V_cruise ** 2 * Sref
    TSFC = TSFC_at_alt(M_cruise, (Thrust / n_eng / eng_scaling), h_cruise)

    Range_cruise = (V_cruise * L_D / TSFC) * np.log(W0 / W1) * 3600

    # Conversions
    conv = 0.000164579
    total = (climbRange + Range_cruise - (V_cruise * 0.75 * 3600)) * conv - 200
    return max(0, total)


# --- Segment 1: Constant Payload (Structural Limit) ---
# Range increases as we add fuel up to MTOW
Wf_at_max_pay = WTO_design - OEW - maxPayload
range_at_max_pay = calcPayloadRange(WTO_design, Wf_at_max_pay / WTO_design, Cd0)

# --- Segment 2: MTOW Limited (Trading Payload for Fuel) ---
# Payload goes from Max to Design, Fuel goes from Wf_at_max to Wf_max, WTO stays constant
payloads_mtow = np.linspace(maxPayload, designPayload, 10)
ranges_mtow = []
for p in payloads_mtow:
    Wf = WTO_design - OEW - p
    ranges_mtow.append(calcPayloadRange(WTO_design, Wf / WTO_design, Cd0))

# --- Segment 3: Fuel Capacity Limited (Trading Payload for Weight) ---
# Fuel stays at Wf_max, Payload goes from Design to 0, WTO decreases
payloads_fuel = np.linspace(designPayload, 0, 10)
ranges_fuel = []
for p in payloads_fuel:
    current_WTO = OEW + Wf_max + p
    ranges_fuel.append(calcPayloadRange(current_WTO, Wf_max / current_WTO, Cd0))

# --- Plotting ---
plt.figure(figsize=(11, 7))

# Plot segments
plt.plot([0, range_at_max_pay], [maxPayload, maxPayload], 'b-', linewidth=3)  # Structural cap
plt.plot(ranges_mtow, payloads_mtow, 'b-', linewidth=3)  # MTOW trade
plt.plot(ranges_fuel, payloads_fuel, 'b-', linewidth=3, label='Flight Envelope')  # Fuel limit

# Points of Interest
plt.scatter([range_at_max_pay, ranges_mtow[-1], ranges_fuel[-1]],
            [maxPayload, designPayload, 0], color='red', zorder=5)

# Labels and Annotations
plt.title('Payload-Range Diagram (Sized Aircraft)', fontsize=14)
plt.xlabel('Range (nmi)', fontsize=12)
plt.ylabel('Payload (lbs)', fontsize=12)

plt.annotate(f'Max Payload Range\n{range_at_max_pay:.0f} nmi',
             xy=(range_at_max_pay, maxPayload), xytext=(range_at_max_pay - 1200, maxPayload + 3000),
             arrowprops=dict(arrowstyle='->'))

plt.annotate(f'Design Point\n{ranges_mtow[-1]:.0f} nmi',
             xy=(ranges_mtow[-1], designPayload), xytext=(ranges_mtow[-1] + 500, designPayload + 5000),
             arrowprops=dict(arrowstyle='->'))

plt.annotate(f'Ferry Range\n{ranges_fuel[-1]:.0f} nmi',
             xy=(ranges_fuel[-1], 0), xytext=(ranges_fuel[-1] - 1000, 5000),
             arrowprops=dict(arrowstyle='->'))

plt.grid(True, alpha=0.3)
plt.xlim(0, max(ranges_fuel) * 1.1)
plt.ylim(0, maxPayload * 1.1)
plt.show()