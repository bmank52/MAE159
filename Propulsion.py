import numpy as np
from scipy.interpolate import LinearNDInterpolator
import pandas as pd

def propulsion(alt, Ma):
    T_max_exist_SLSD = np.polyval([ -2.32298858,  38.88677337, -47.75554851,  45.36765101], 0) * 1000
    if alt <=15000:
        Thrust_max_SL = np.polyval([ -2.32298858,  38.88677337, -47.75554851,  45.36765101], Ma) * 1000
        Thrust_max_15k = np.polyval([12.8202115,  -35.99705866,  39.94062197, -28.2682791,   25.54563471], Ma) * 1000
        Thrust_max_alt = np.interp(alt, [0, 15000], [Thrust_max_SL, Thrust_max_15k])
    elif alt <=35000:
        Thrust_max_15k = np.polyval([12.8202115,  -35.99705866,  39.94062197, -28.2682791,   25.54563471], Ma) * 1000
        Thrust_max_35k = np.polyval([31.37125602, -113.55096428,  142.71282744,  -72.82695247,   22.1910169], Ma) * 1000
        Thrust_max_alt = np.interp(alt, [15000, 35000], [Thrust_max_15k, Thrust_max_35k])
    elif alt <=45000:
        Thrust_max_45k = np.polyval([-25.98868099,  70.37982565, -66.17181629,  26.96109535,   1.61003537], Ma) * 1000
        Thrust_max_35k = np.polyval([31.37125602, -113.55096428, 142.71282744, -72.82695247, 22.1910169], Ma) * 1000
        Thrust_max_alt = np.interp(alt, [35000, 45000], [Thrust_max_35k, Thrust_max_45k])
        """
        coeff_jt9d_15k = {
            0.3: [-1.11020742e-05, 1.53877413e-04, 1.95151635e-04, 2.27849365e-02],
            0.35: [7.16837039e-06, -8.97816486e-04, 2.02239404e-02, -1.29398699e-03],
            0.4: [-1.58160820e-05, -9.52227392e-05, 1.40060637e-02, 9.96421708e-02],
            0.45: [2.40838224e-05, -2.32270847e-03, 5.45930664e-02, -2.88839477e-02],
            0.5: [4.49277461e-05, -2.85950743e-03, 5.72179797e-02, 7.99909361e-02],
            0.55: [6.28851214e-05, -3.70328329e-03, 7.14305615e-02, 9.70454668e-02],
            0.6: [8.59073388e-05, -4.34853523e-03, 8.05300530e-02, 1.31717426e-01],
            0.65: [1.12694012e-04, -5.37410220e-03, 9.61713773e-02, 1.41477676e-01],
            0.7: [0.000163, -0.00685019, 0.11337742, 0.15281292],
            0.75: [1.43534016e-04, -6.77083747e-03, 1.22644425e-01, 1.66647449e-01],
            0.8: [0.00048282, -0.01412485, 0.17544895, 0.11497159],
            0.9: [0.00105616, -0.02071407, 0.21063517, 0.12884251],
            1: [0.0060614, -0.08252494, 0.45504579, -0.04896651],
            1.5: [0.01084076, -0.1328488, 0.65126145, 0.01357356],

        }
        coeff_jt9d_35k = {
            0.45: [-2.94821394e-05, -1.10179393e-02, 1.48759954e-01, -4.90473020e-02],
            0.5: [0.00038899, -0.01540286, 0.15302975, 0.09680926],
            0.55: [0.00027982, -0.0142024, 0.1553464, 0.18350829],
            0.6: [0.00044929, -0.0173512, 0.18188532, 0.22015463],
            0.65: [0.00060831, -0.02084709, 0.21770461, 0.19981112],
            0.68: [-0.0016583, 0.03044437, -0.16355466, 1.20890579],
            0.7: [0.00063145, -0.02165827, 0.23535975, 0.24092355],
            0.75: [0.00345229, -0.05422091, 0.3678761, 0.15090658],
            0.8: [-0.0053525, 0.02995054, 0.14096054, 0.3735979],
            0.9: [-0.00525167, -0.02321845, 0.38819898, 0.19326823],
            0.95: [0.05036421, -0.39011683, 1.16343076, -0.196837],
            1.05: [0.1034898, -0.68391613, 1.62823897, -0.29707568],
        }
        """
    lapse = Thrust_max_alt / T_max_exist_SLSD
    return [Thrust_max_alt,lapse]

def calc_TSFC(M, T, f):
    df = pd.read_csv(f, header=None)
    all_data = []
    for i in range(0, df.shape[1], 2):
        tsfc_val = float(df.iloc[0, i])
        mach_cords = pd.to_numeric(df.iloc[2:, i], errors='coerce')
        thrust_coords = pd.to_numeric(df.iloc[2:, i + 1], errors='coerce')

        temp_df = pd.DataFrame({
            'mach': mach_cords,
            'thrust': thrust_coords,
            'tsfc': tsfc_val,
        }).dropna()

        all_data.append(temp_df)

    final_df = pd.concat(all_data, ignore_index=True)

    # Prepare inputs (Mach, Thrust) and targets (TSFC)
    points = final_df[['mach', 'thrust']].values
    values = final_df['tsfc'].values

    # Build the interpolator
    # This creates a surface representing TSFC over the Mach-Thrust plane
    get_tsfc = LinearNDInterpolator(points, values)
    return float(get_tsfc(M, T))

def TSFC_at_alt(M, T, alt):
    T = T/1000
    if alt <= 15000:
        TSFC_SL = calc_TSFC(M, T, 'Plots/JT9D_SL_TSFC.csv')
        TSFC_15k = calc_TSFC(M, T, 'Plots/JT9D 15k.csv')
        TSFC = np.interp(alt, [0, 15000], [TSFC_SL, TSFC_15k])
    elif alt <= 35000:

        TSFC_15k = calc_TSFC(M, T, 'Plots/JT9D 15k.csv')
        TSFC_35k = calc_TSFC(M, T, 'Plots/JT9D 35k.csv')
        TSFC = np.interp(alt, [15000, 35000], [TSFC_15k, TSFC_35k])

    return TSFC


# --- TESTING BLOCK ---
if __name__ == "__main__":
    print("=== Propulsion Module Diagnostic Test ===")

    # Define your design parameters here for the test
    n_eng = 2
    engine_scaling = 1.0  # Change this to your S factor (e.g. 1.1 or 1.5)

    print(f"\nConfiguration: {n_eng} Engines | Scaling Factor: {engine_scaling}")

    test_cases = [
        # (Mach, Total_Aircraft_Thrust, Alt)
        (0.6, 15000, 17500),
        (0.8, 14000, 35000),
    ]

    for m, t_total, a in test_cases:
        # Calculate thrust per engine (unscaled) for lookup
        t_per_eng_unscaled = t_total / (n_eng * engine_scaling)

        # Check Max Available
        t_max_unscaled, _ = propulsion(a, m)
        t_max_scaled_total = t_max_unscaled * n_eng * engine_scaling

        print(f"\n--- Testing Alt: {a}ft, Mach: {m} ---")
        print(f"Total Aircraft Thrust Required: {t_total:.1f} lbs")
        print(f"Total Aircraft Max Available: {t_max_scaled_total:.1f} lbs")

        if t_total > t_max_scaled_total:
            print(">> ERROR: Thrust Required exceeds Aircraft Capability!")

        # Perform lookup
        result = TSFC_at_alt(m, t_per_eng_unscaled, a)
        print(f"Lookup Thrust (Unscaled, Per-Eng): {t_per_eng_unscaled:.1f} lbs")
        print(f"TSFC Result: {result}")

    print("\n==========================================")
