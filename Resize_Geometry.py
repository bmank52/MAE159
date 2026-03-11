import numpy as np


def resize_geometry(W, W_S, AR, sweep, pax =250,  taper=0.35):
    S_ref = W / W_S #calc Sref
    b_ref = np.sqrt(S_ref * AR) #calc span
    Cr = 2 * S_ref / (b_ref * (1 +taper)) #calc root chord
    Ct = Cr * taper #calc tip chord
    mac = 2 / 3 * Cr * (taper**2 + taper + 1) / (taper + 1) #mean chord
    y_mac = b_ref / 6 * (2*taper + 1) / (taper + 1) #position of mean chord
    mac_quarter_c = np.tan(np.radians(sweep)) * y_mac + Cr/4

    abreast = 6
    aisle = 1
    L_f = 2.67 * pax / abreast + .36 * pax + 6.4
    D_f = 1.75 * abreast + 1.58 * aisle + 1.0

    return [S_ref, mac, b_ref, Cr, Ct, mac_quarter_c, L_f, D_f]


print(resize_geometry(441405, 141, 8,40,  250, 0.35))