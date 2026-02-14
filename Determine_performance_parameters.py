import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

from approach_speed import iterate_W_S_approach
from Landing_Field_Length import iterate_W_S_LND
from Takeoff_field_length import takeoff_field_length
from Cruise_Thrust_Required import Cruise_Thrust_Required
from Service_Ceiling import service_ceiling
from Climb import climb_gradient




def determine_performance_parameters(W_S_guess, M_cruise, W_S_range, sweep, AR, Cdo, landing_approach_speed=140, range=7000, temp_delta=22.6, cruise_alt=35000, max_landing_fuel_ratio=0.45, field_length=9000, n_eng=2, ceiling_alt=40000):
    # climb gradients
    first_TO_climb = {
        "V_Vstall": 1.2,
        "Gear": True,
        "Flaps": "TO",
        "alt": 0,
        "Weight": "MTOW",
        "OEI": True,
        "climb_gradient_2_eng": 0,
        "climb_gradient_3_eng": 0.3,
        "climb_gradient_4_eng": 0.5,
    }

    second_TO_climb = {
        "V_Vstall": 1.2,
        "Gear": False,
        "Flaps": "TO",
        "alt": 0,
        "Weight": "MTOW",
        "OEI": True,
        "climb_gradient_2_eng": 2.4,
        "climb_gradient_3_eng": 2.7,
        "climb_gradient_4_eng": 3.0,
    }

    third_TO_climb = {
        "V_Vstall": 1.2,
        "Gear": False,
        "Flaps": False,
        "alt": 1000,
        "Weight": "MTOW",
        "OEI": True,
        "climb_gradient_2_eng": 1.2,
        "climb_gradient_3_eng": 1.5,
        "climb_gradient_4_eng": 1.7,
    }

    approach_go_around = {
        "V_Vstall": 1.4,
        "Gear": False,
        "Flaps": "TO",
        "alt": 0,
        "Weight": "MLNDW",
        "OEI": True,
        "climb_gradient_2_eng": 2.1,
        "climb_gradient_3_eng": 2.4,
        "climb_gradient_4_eng": 2.7,
    }

    Landing_go_around = {
        "V_Vstall": 1.3,
        "Gear": True,
        "Flaps": "LND",
        "alt": 0,
        "Weight": "MLNDW",
        "OEI": False,
        "climb_gradient_2_eng": 3.2,
        "climb_gradient_3_eng": 3.2,
        "climb_gradient_4_eng": 3.2,
    }


    ### Constraint Diagram
    plt.figure(figsize=(10, 6))
    W_S_Approach = iterate_W_S_approach(W_S_guess, M_cruise, sweep, AR, landing_approach_speed, range, temp_delta,
                                        cruise_alt, max_landing_fuel_ratio)  # calc approach W_S limit
    W_S_LNDFL = iterate_W_S_LND(W_S_guess, M_cruise, sweep, AR, cruise_alt, Cdo, field_length, max_landing_fuel_ratio,
                                range)  # calc landing W_S limit
    T_W_TOFL = [takeoff_field_length(ws, sweep, AR, n_eng, M_cruise, cruise_alt, range, field_length)
                for ws in W_S_range]  # calc range of T_W for TOFL based on a range of W_S
    T_W_Cruise_Thrust = [Cruise_Thrust_Required(ws, AR, M_cruise, cruise_alt)
                         for ws in W_S_range]
    T_W_service_ceiling = [service_ceiling(ws, ceiling_alt, cruise_alt, AR, M_cruise)
                           for ws in W_S_range]
    T_W_climb_first = [climb_gradient(ws, first_TO_climb, range, AR, sweep, M_cruise, cruise_alt)
                       for ws in W_S_range]
    T_W_climb_second = [climb_gradient(ws, second_TO_climb, range, AR, sweep, M_cruise, cruise_alt)
                        for ws in W_S_range]
    T_W_climb_third = [climb_gradient(ws, third_TO_climb, range, AR, sweep, M_cruise, cruise_alt)
                       for ws in W_S_range]
    T_W_climb_approach = [climb_gradient(ws, approach_go_around, range, AR, sweep, M_cruise, cruise_alt)
                          for ws in W_S_range]
    T_W_climb_landing = [climb_gradient(ws, Landing_go_around, range, AR, sweep, M_cruise, cruise_alt)
                         for ws in W_S_range]

    tick_effect = [path_effects.Normal(), path_effects.TickedStroke(angle=60, length=1, spacing=10)] #for vertical lines
    plt.axvline(x=W_S_Approach, color='red', label='Approach', path_effects=tick_effect)  # plt approach limit
    plt.axvline(x=W_S_LNDFL, color='blue', label='LNDFL',path_effects=tick_effect)  # plt landing limit
    down_tick = [path_effects.Normal(), path_effects.TickedStroke(angle=-60, length=1, spacing=10)] #for curves below design space
    plt.plot(W_S_range, T_W_TOFL, color='green', label='TOFL', path_effects=down_tick)
    plt.plot(W_S_range, T_W_Cruise_Thrust, color='c', label='CRUISE Thrust Required', path_effects=down_tick)
    plt.plot(W_S_range, T_W_service_ceiling, color='m', label='Service ceiling', path_effects=down_tick)
    plt.plot(W_S_range, T_W_climb_first, color='y', label='First climb', path_effects=down_tick)
    plt.plot(W_S_range, T_W_climb_second, ls='dashed', color='r', label='Second climb', path_effects=down_tick)
    plt.plot(W_S_range, T_W_climb_third, color='k', label='Third climb', path_effects=down_tick)
    plt.plot(W_S_range, T_W_climb_approach, ls='dashed', color='b', label='Approach', path_effects=down_tick)
    plt.plot(W_S_range, T_W_climb_landing, ls='dashed', color='g', label='Landing', path_effects=down_tick)


    plt.xlabel(r'$\frac{W}{S} \ [lb/ft^2]$')
    plt.ylabel(r'$\frac{T}{W}$')
    plt.title(f'Design Envelope for Sweep = {sweep} and AR = {AR}')
    plt.grid()
