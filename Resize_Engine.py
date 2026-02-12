


def resize_engine(W, T_W, n_eng=2):
    T_SLSD = W * T_W
    T_SLSD_1_eng = T_SLSD / n_eng
    eng_scaling = T_SLSD_1_eng / 45500
    return eng_scaling
