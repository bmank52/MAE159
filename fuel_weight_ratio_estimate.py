from ambiance import Atmosphere
import numpy as np

def fuel_weight_ratio_estimate(range, M_cruise, altitude):   #range in nmi, alt in ft
    coeffes = [5.66594337e-13, -1.23328283e-08, 1.25236419e-04, 6.14364245e-03]  #from plotting script
    v_kts = M_cruise * Atmosphere(altitude * 0.3048).speed_of_sound * 1.94384 # Converts M to kts
    all_out_range = range + 200 + .75 * v_kts # Mission range + 200 nmi + 45mins cruise speed
    return np.polyval(coeffes, all_out_range)
