import numpy as np


def resize_geometry(W, W_S, AR, sweep, taper=0.2):
    S_ref = W / W_S #calc Sref
    b_ref = np.sqrt(S_ref * AR) #calc span
    Cr = 2 * S_ref / (b_ref * (1 +taper)) #calc root chord
    Ct = Cr * taper #calc tip chord
    mac = 2 / 3 * Cr * (taper**2 + taper + 1) / (taper + 1) #mean chord
    y_mac = b_ref / 6 * (2*taper + 1) / (taper + 1) #position of mean chord
    mac_quarter_c = np.tan(np.radians(sweep)) * y_mac + Cr/4

    return [S_ref, mac, b_ref, Cr, Ct, mac_quarter_c]