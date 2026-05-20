from CHSP_GRandF import GRandF_CHSP
from HCP_GRandF import GRandF_HCP
from RC_GRandF import GRandF_RC
from Calibrated_Variables import return_calib_var


def Delta_W_status(W_, H_, Hstate_tp1, tau1, tau2_HCP4, tau2_RC):
    G_CHSP = GRandF_CHSP(W_)[0]
    if Hstate_tp1 == 1:
        return 0
    if Hstate_tp1 == 2:
        return 0
    if Hstate_tp1 == 3:
        G_HCPm = GRandF_HCP(W_, 'medium')[0]
        G_HCPh = GRandF_HCP(W_, 'high')[0]
        diff1 = (G_HCPm - G_CHSP) * min(tau1, tau2_HCP4)
        diff2 = (G_HCPh - G_HCPm) * tau2_HCP4
        return diff1 + diff2
    if Hstate_tp1 == 5:
        Leasing = return_calib_var()[5]
        G_RC = GRandF_RC(W_, H_, Leasing)[0]
        return (G_RC - G_CHSP) * tau2_RC