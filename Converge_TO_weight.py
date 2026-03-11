import numpy as np
import matplotlib.pyplot as plt


def calc_TO_weight (Wf_Wto, W_S, W_TO, T_W, AR, taper, t2c, sweep, pax, payload, n_eng=2):

    ###Constants used to calc OEW
    n=1.5 * 2.5 #ultimate load factor
    Kw = 1.0 #1.0 for wing mounted eng
    abreast = 9
    asiles = 2
    Kf = 11.5 #for PAXX> 135
    Ktails = 0.17 # for wing engines
    N_crew = 2
    N_stew = 4

    W_wing = (.00945 * W_TO ** 1.195 * AR ** .8 * (1 + taper) ** .25 )\
             / ((t2c + 0.03 )** 0.4 * np.cos(np.radians(sweep)) * W_S ** .695) * Kw * n ** .5 #wing weight eqn

    L_fuselage = 2.67 * pax/abreast + 0.36*pax + 6.4 #fuselage length
    d_fuselage = 1.75 * abreast + 1.58 * asiles + 1.0 #diameter fuselage
    L_fuselage = 203.6
    d_fuselage = 19.2
    W_fuselage = .6727 * Kf * W_TO ** .235 * L_fuselage ** .6 * d_fuselage **.72 * n ** .3 #fuselage weight

    W_gear = 0.040 * W_TO #landing gear weight
    W_nacelles_pylons = 0.0555 * T_W * W_TO #nacelle and pylon weight
    W_tails = Ktails * W_wing #tails weight
    W_engines = W_TO / (3.58 / T_W) #weight of engines

    W_fuel = 1.0275 * Wf_Wto * W_TO
    W_tank = .0175 * W_fuel
    W_unuseable_fuel = .01 * W_fuel
    W_tanks_unuseable_fuel = W_tank + W_unuseable_fuel
    W_equipment = 132 * pax + 300 * n_eng + 0.035 * W_TO + 260 * N_crew + 170 * N_stew

    #adjustments for CF
    W_wing = W_wing * .7
    W_tails = W_tails * .7
    W_fuselage = W_fuselage * .85
    W_equipment = W_equipment * .9
    W_nacelles_pylons = W_nacelles_pylons * .8


    OEW = W_wing + W_tails + W_fuselage + W_gear + W_nacelles_pylons + W_engines + W_tanks_unuseable_fuel + W_equipment
    W_TO_new = OEW  + W_fuel + payload
    return W_TO_new

def converge_TO_weight(Wf_Wto, W_S, T_W, AR, taper, t2c, sweep, pax, cargo):
    payload = pax * 215 + cargo  # weight of passengers and cargo
    W_TO = 500000
    W_TO_old = 0# guess weight

    while np.abs(W_TO - W_TO_old) > 5:
        W_TO_old = W_TO
        W_TO = calc_TO_weight(Wf_Wto, W_S, W_TO_old, T_W, AR, taper, t2c, sweep, pax, payload)

    return W_TO

def calc_weight_fractions(W_TO, Wf_WTO, T_W, AR, taper, sweep, t2c, W_S, Lf, Df):
    ###Constants used to calc OEW
    n = 1.5 * 2.5  # ultimate load factor
    Kw = 1.0  # 1.0 for wing mounted eng
    Kf = 11.5  # for PAXX> 135
    Ktails = 0.17  # for wing engines
    N_crew = 2
    N_stew = 4

    n_eng = 2
    pax = 250
    payload = pax * 215 + 12000

    W_wing = (.00945 * W_TO ** 1.195 * AR ** .8 * (1 + taper) ** .25) \
             / ((t2c + 0.03) ** 0.4 * np.cos(np.radians(sweep)) * W_S ** .695) * Kw * n ** .5  # wing weight eqn

    L_fuselage = Lf
    d_fuselage = Df
    W_fuselage = .6727 * Kf * W_TO ** .235 * L_fuselage ** .6 * d_fuselage ** .72 * n ** .3  # fuselage weight

    W_gear = 0.040 * W_TO  # landing gear weight
    W_nacelles_pylons = 0.0555 * T_W * W_TO  # nacelle and pylon weight
    W_tails = Ktails * W_wing  # tails weight
    W_engines = W_TO / (3.58 / T_W)  # weight of engines

    W_fuel = 1.0275 * Wf_WTO * W_TO
    W_tank = .0175 * W_fuel
    W_unuseable_fuel = .01 * W_fuel
    W_tanks_unuseable_fuel = W_tank + W_unuseable_fuel

    W_equipment = 132 * pax + 300 * n_eng + 0.035 * W_TO + 260 * N_crew + 170 * N_stew


    # adjustments for CF
    W_wing = W_wing * .7
    W_tails = W_tails * .7
    W_fuselage = W_fuselage * .85
    W_equipment = W_equipment * .9
    W_nacelles_pylons = W_nacelles_pylons * .8

    print(f'Equipment Weight: {W_equipment}')
    print(f'Tanks Weight: {W_tanks_unuseable_fuel}')
    print(f'Fuel Weight: {W_fuel}')
    print(f'Engines Weight: {W_engines}')
    print(f'Tails Weight: {W_tails}')
    print(f'Nacelles/Pylons Weight: {W_nacelles_pylons}')
    print(f'Gear Weight: {W_gear}')
    print(f'Fuselage Weight: {W_fuselage}')
    print(f'Wing Weight: {W_wing}')

    W_strucutres = W_wing + W_tails + W_fuselage + W_gear + W_nacelles_pylons
    W_systems = W_equipment + W_tanks_unuseable_fuel


    OEW = W_wing + W_tails + W_fuselage + W_gear + W_nacelles_pylons + W_engines + W_tanks_unuseable_fuel + W_equipment
    W_TO_new = OEW + W_fuel + payload


    weight_components = [W_strucutres, W_systems, W_engines, W_fuel, payload]
    weight_chart_labels = ['Structures', 'Systems', 'Engines', 'Fuel', 'Payload']

    # Create a function to format the labels
    def fmt_labels(pct):
        # pct is the percentage Matplotlib calculates automatically
        # total is the sum of our weight components
        total = sum(weight_components)
        val = int(round(pct * total / 100.0))
        return f'{pct:.1f}%\n({val} lbs)'

    plt.pie(weight_components, labels=weight_chart_labels, autopct=fmt_labels)
    plt.title('Aircraft MTOW Weight Distribution')
    plt.show()

    print(f"Total Takeoff Weight: {W_TO_new:.2f} lbs")
    print('-' * 30)
    print(f"Structural Weight: {W_strucutres:.2f} lbs")
    print(f"Systems Weight: {W_systems:.2f} lbs")
    print(f"Propulsion Weight: {W_engines:.2f} lbs")
    print(f"Fuel Weight {W_fuel:.2f} lbs")
    print(f"Payload Weight: {payload:.2f} lbs")


    return W_TO_new

#print(converge_TO_weight(.40563, 141, .31, 8, .35, .179, 40, 250, 12000))
calc_weight_fractions(441404, .40563, .31, 8, .35, 40, .179, 141, 203.6, 19.2)