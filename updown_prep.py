from FIstatus import I_status, F_status
from DeltaW import Delta_W_status
from Calibrated_Variables import return_calib_var

def derivatives_tp1(W_, H_, Hstate_):
    Up = I_status(W_+10, H_, Hstate_)-F_status(W_+10, H_, Hstate_)
    Down = I_status(W_-10, H_, Hstate_)-F_status(W_-10, H_, Hstate_)
    return (Up-Down)/20

def direct2EI(EI_tm1, direction):
    if direction == 'up':
        EI_t = EI_tm1 + 1
    if direction == 'down':
        EI_t = EI_tm1
    return EI_t


def Hstate2Cf(Hstate):
    if Hstate != 5:
        C_f_t = 10000
    if Hstate == 5:
        C_f_t = 17961
    return C_f_t


def reVC(W_tp1, EI_t, Hstate, Dict_interp_tp1):
    V_interpolated = Dict_interp_tp1['V'][Hstate][EI_t]
    C_interpolated = Dict_interp_tp1['C'][Hstate][EI_t]
    V = V_interpolated(W_tp1).item()
    C = C_interpolated(W_tp1).item()
    return V, C


def Compare35(W_tp1, H_t, alpha, t, V3, C3, V5, C5):
    C_low = 10000
    C_RACF = 17961
    H_ini, W_ini, tau1_arr, tau2_HCP4_arr, tau2_RC_arr, Leasing = return_calib_var(alpha)
    if V5 >= V3:
        V3s = V5
        C3s = C5
        mu3s = 1 + derivatives_tp1(max(W_tp1 - Delta_W_status(W_tp1, H_t, 5, tau1_arr[t], tau2_HCP4_arr[t], tau2_RC_arr[t]),  C_RACF + 10), H_t, 5)
        I_RACF = 1
        return V3s, C3s, mu3s,I_RACF
    if V5 < V3:
        V3s = V3
        C3s = C3
        mu3s = 1 + derivatives_tp1(max(W_tp1 - Delta_W_status(W_tp1, H_t, 3, tau1_arr[t], tau2_HCP4_arr[t], tau2_RC_arr[t]), C_low + 10), H_t, 3)
        I_RACF = 0
        return V3s, C3s, mu3s, I_RACF