import numpy as np

def return_calib_var(alpha = 0.5):
    Leasing = 1
    W = 1200000
    H = W * alpha/(alpha+1)
    tau1_arr = np.full(41, 1/6)
    tau2_HCP4 = np.full(41, 3/4)
    tau2_RC = np.full(41, 1/24)
    return H, W/(1+alpha), tau1_arr, tau2_HCP4, tau2_RC, Leasing


