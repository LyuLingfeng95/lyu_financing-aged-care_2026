from CHSP_GRandF import GRandF_CHSP
from HCP_GRandF import GRandF_HCP
from RC_GRandF import GRandF_RC
from Calibrated_Variables import return_calib_var
from age_pension import calculate_pension_income


def F_status(W_, H_, Hstate):
    if Hstate == 1:
        return 0
    if Hstate == 2:
        return GRandF_CHSP(W_)[1]
    if Hstate == 3:
        F_HCPh = GRandF_HCP(W_, 'high')[1]
        return F_HCPh
    if Hstate == 5:
        Leasing = return_calib_var()[5]
        F_RC = GRandF_RC(W_, H_, Leasing)[1]
        return F_RC



def I_status(W_, H_, Hstate):
    if Hstate == 1:
        return calculate_pension_income(W_)
    if Hstate == 2:
        return calculate_pension_income(W_)
    if Hstate == 3:
        return calculate_pension_income(W_)
    if Hstate == 5:
        Leasing = return_calib_var()[5]
        if Leasing == 1:
            return calculate_pension_income(W_, 0.04 * H_) + 0.04 * H_
        if Leasing == 0:
            return calculate_pension_income(W_)