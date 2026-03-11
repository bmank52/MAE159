import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

mac = 21.3
L_fus = 204.3
w_fus = 42259.82021124542
x_wing = L_fus * 0.405 #Vary this
w_wing = 31780.48244806755
D_nacelle = 10.7
L_nacelle = 19.4
x_nac = x_wing - 2 * D_nacelle + 0.4 * L_nacelle
w_eng_nac = 6075.4846560000005 + 38222.134078212286
w_tanks = 5059.18844459325
w_tails = 5402.682016171484
w_payload = 215 * 250 + 12000
w_fuel = 183970.4888943
w_gear_equip = 17656.16 + 45224.226


Sref = 3130
b_ref = 158.3
AR_wing = 8
AR_htail = 4
M_cruise = 0.85
sweep = 40
d_fus = 19.2

def calc_CG(x_wing, w_wing, L_fus, w_fus, x_nac, w_eng_nac, w_tanks, w_tails, w_payload, w_fuel, w_gear_equip, mac):
    ### Calcs X and Z pos for CG using nose as x=0 and bottom of fuselage as z = 0 ###
    x_wing_cg = x_wing + .25 * mac
    x_fusealge = 0.4 * L_fus
    x_tail = 0.95 * L_fus
    x_payload = 0.5 * L_fus
    sum_of_moments= x_wing_cg * w_wing + x_fusealge * w_fus + x_nac * w_eng_nac + w_tanks * x_wing_cg + x_tail * w_tails + x_payload * w_payload + x_wing_cg * w_fuel
    sum_of_weights = w_wing + w_fus + w_eng_nac + w_tanks + w_tails + w_payload + w_fuel
    x_cg = sum_of_moments / sum_of_weights

    sum_of_moments_MTOW = sum_of_moments + x_cg * w_gear_equip
    sum_of_weights_MTOW = sum_of_weights + w_gear_equip
    x_CG_MTOW = sum_of_moments_MTOW / sum_of_weights_MTOW
    x_gear_equipment = x_CG_MTOW #place gear at MTOW CG
    print(f'X CG MTOW: {x_CG_MTOW}')

    OEW = sum_of_weights_MTOW - w_payload - w_fuel #opperating empty weight = no fuel no payload
    sum_of_moments_OEW = x_wing_cg * w_wing + x_fusealge * w_fus + x_nac * w_eng_nac + w_tanks * x_wing_cg + x_tail * w_tails + x_gear_equipment * w_gear_equip

    x_CG_OEW = sum_of_moments_OEW / OEW
    print(f'X CG OEW: {x_CG_OEW}')

    return x_CG_MTOW, x_CG_OEW


def make_scissor_plot(mac, AR_wing, M_cruise, sweep, d_fus,  b_ref, Sref, AR_htail, x_wing, w_wing, L_fus, w_fus, x_nac, w_eng_nac, w_tanks, w_tails, w_payload, w_fuel, w_gear_equip):
    x_CG_MTOW, x_CG_OEW = calc_CG(x_wing, w_wing, L_fus, w_fus, x_nac, w_eng_nac, w_tanks, w_tails, w_payload, w_fuel, w_gear_equip, mac)
    x_CG_MTOW_bar = (x_CG_MTOW - x_wing)/ mac
    x_CG_OEW_bar = (x_CG_OEW - x_wing) / mac
    x_mac_bar = x_wing / mac
    x_tail = 0.95 * L_fus

    eta = 0.9
    beta = np.sqrt(1 - M_cruise ** 2)
    sweep = np.radians(sweep)
    CLa_wing = (2 * np.pi * AR_wing) / (2 + np.sqrt(4 + (AR_wing * beta) ** 2 * (1 + (np.tan(sweep)/beta)**2) )) #wing lift curve slop
    CLa_wing_body = CLa_wing * (1 + 2.15 * d_fus/b_ref)#fusealge contribution
    CLa_htail = (2 * np.pi * AR_htail) / (2 + np.sqrt(4 + (AR_htail * beta/eta) ** 2 * (1 + (np.tan(sweep)/beta)**2) )) #htail lift curve slope

    Kf = 0.01
    Wf = d_fus
    Cma_fus = Kf * Wf ** 2 * L_fus / mac / Sref  * np.pi / 180 #given per deg but we need rad

    downwash = 0.65

    X_ac_htail_bar = (x_tail - x_wing) / mac

    X_bar_np_10 = (CLa_wing_body * 0.25 - Cma_fus + eta * .1 * CLa_htail * (1-downwash) * X_ac_htail_bar) / (CLa_wing_body + eta * .1 * CLa_htail * (1-downwash)) #guess NP for tail ratio of 0.1
    X_bar_np_30 = (CLa_wing_body * 0.25 - Cma_fus + eta * .3 * CLa_htail * (1-downwash) * X_ac_htail_bar) / (CLa_wing_body + eta * .3 * CLa_htail * (1-downwash))  # guess NP for tail ratio of 0.3

    CL_max = 3.31
    X_tail_bar = x_tail / mac
    aoa = 20 * np.pi/180 #20 degs in rads
    delta_e = -25 * np.pi / 180 #25 degress in rads
    ke = 0.3 #ratio of elevator chord to htail
    Cm_fus = Cma_fus * aoa
    partial_alpha_0_lift_partial_delta_elevator = - (1.576 * ke ** 3 - 3.458 * ke **2 + 2.882 * ke)
    CL_htail = CLa_htail * (aoa * (1- downwash) - partial_alpha_0_lift_partial_delta_elevator * delta_e)
    Cm_CG_10 = CL_max * (x_CG_MTOW_bar - 0.25) + Cm_fus - eta * .1 * CL_htail * (X_ac_htail_bar - x_CG_MTOW_bar)
    Cm_CG_30 = CL_max * (x_CG_MTOW_bar - 0.25) + Cm_fus - eta * .3 * CL_htail * (X_ac_htail_bar - x_CG_MTOW_bar)

    x_cg_forward_bar_10 = - (Cm_fus - CL_max * .25 - (eta * .1 * CL_htail) * X_ac_htail_bar) / (CL_max + eta *.1 * CL_htail)
    x_cg_forward_bar_30 = - (Cm_fus - CL_max * .25 - (eta * .3 * CL_htail) * X_ac_htail_bar) / (CL_max + eta * .3 * CL_htail)

    #plotting
    sh_s_ratios = [0.1, 0.3]
    np_limits = [X_bar_np_10, X_bar_np_30]
    SM_10_limits = [X_bar_np_10 - .1, X_bar_np_30 - .1]
    fwd_limits = [x_cg_forward_bar_10, x_cg_forward_bar_30]

    #min tail size
    target_cg_range = 0.20

    # 1. Fly to Stall limit (Forward Limit) slope & intercept
    a_fs = (0.3 - 0.1) / (x_cg_forward_bar_30 - x_cg_forward_bar_10)
    b_fs = 0.1 - a_fs * x_cg_forward_bar_10

    # 2. 10% Static Margin limit (Aft Limit) slope & intercept
    SM10_limit_10 = X_bar_np_10 - 0.1
    SM10_limit_30 = X_bar_np_30 - 0.1
    a_sm10 = (0.3 - 0.1) / (SM10_limit_30 - SM10_limit_10)
    b_sm10 = 0.1 - a_sm10 * SM10_limit_10

    # 3. Solve for S_min where the horizontal gap is exactly target_cg_range
    S_min = (target_cg_range + (b_sm10 / a_sm10) - (b_fs / a_fs)) / ((1 / a_sm10) - (1 / a_fs))

    # 4. X-coordinates for plotting the horizontal line
    x_fwd_min = (S_min - b_fs) / a_fs
    x_aft_min = (S_min - b_sm10) / a_sm10

    plt.figure(figsize=(10, 6))

    #Tick Lines
    right_effect = [path_effects.Normal(), path_effects.TickedStroke(angle=-30, length=1, spacing=10)]
    left_effect = [path_effects.Normal(), path_effects.TickedStroke(angle=60, length=1, spacing=10)]
    down_effect = [path_effects.Normal(), path_effects.TickedStroke(angle=-60, length=1, spacing=10)]

    # Plot Limits
    plt.plot(np_limits, sh_s_ratios, label='X Neutral Point', marker='o', color='blue', path_effects=right_effect)
    plt.plot(fwd_limits, sh_s_ratios, label='Fly to Stall', marker='o', color='red', path_effects=left_effect)
    plt.plot(SM_10_limits, sh_s_ratios, label='10% Static Margin', marker='o', color='green', path_effects=right_effect)
    plt.plot([x_fwd_min, x_aft_min], [S_min, S_min], color='darkred', label=f'Min Tail Size: {S_min:.3f}', path_effects=down_effect)

    # Plot actual CG values
    plt.axvline(x=x_CG_MTOW_bar, color='green', linestyle='--', label=f'Actual CG MTOW ({x_CG_MTOW_bar:.2f})')
    plt.axvline(x=x_CG_OEW_bar, color='orange', linestyle='--', label=f'Actual CG OEW ({x_CG_OEW_bar:.2f})')

    plt.xlabel('CG Position ($x/MAC$)', fontsize=12)
    plt.ylabel('Tail Area Ratio ($S_h / S$)', fontsize=12)
    plt.title('Aircraft Scissor Plot', fontsize=14)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.show()

calc_CG(x_wing, w_wing, L_fus, w_fus, x_nac, w_eng_nac, w_tanks, w_tails, w_payload, w_fuel, w_gear_equip, mac)
make_scissor_plot(mac, AR_wing, M_cruise, sweep, d_fus, b_ref, Sref, AR_htail, x_wing, w_wing, L_fus, w_fus,x_nac, w_eng_nac, w_tanks, w_tails, w_payload, w_fuel, w_gear_equip)
