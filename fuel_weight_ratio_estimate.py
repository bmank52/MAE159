from ambiance import Atmosphere
import numpy as np

def fuel_weight_ratio_estimate(range, M_cruise, altitude):   #range in nmi, alt in ft
    coeffes = [-1.41529254e-16,  2.80295568e-12, -2.36029738e-08,  1.44543179e-04, -8.94132729e-04]  #from plotting script
    v_kts = M_cruise * Atmosphere(altitude * 0.3048).speed_of_sound[0] * 1.94384 # Converts M to kts
    all_out_range = range + 200 + .75 * v_kts # Mission range + 200 nmi + 45mins cruise speed
    return np.polyval(coeffes, all_out_range) * 0.782
