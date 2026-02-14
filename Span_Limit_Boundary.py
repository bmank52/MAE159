import numpy as np
from scipy.interpolate import interp1d

def span_limit_boundary(W_S_range, T_W_range, W_TO_grid, AR):   #input range of W/S, T/W, and W_TO
    b_max = 214 #ft  set by gate size
    S_max = b_max ** 2 / AR  #calc bax wing area based on AR and gate span limit

    T_W_boundary = []
    valid_W_S = []


    #for W/S value, find T/W that matches W_TO_limit
    for i, WS in enumerate(W_S_range):
        W_TO_limit = WS * S_max #for the given WS calc make weight
        weight_at_WS = W_TO_grid[i,:] #for the W_S value get all take off weights

        if weight_at_WS.min() <=W_TO_limit <= weight_at_WS.max(): #if the W_TO_limit is in the range of weights for a W/S range
            interp_function = interp1d(weight_at_WS, T_W_range, kind='linear') #create interp function
            #interpolate the data to find what T_W and W_S correspond to the Weight limit
            T_W_needed = interp_function(W_TO_limit)

            T_W_boundary.append(T_W_needed)
            valid_W_S.append(WS)

    return np.array(valid_W_S), np.array(T_W_boundary)



    