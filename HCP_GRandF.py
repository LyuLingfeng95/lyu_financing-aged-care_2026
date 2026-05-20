from age_pension import calculate_pension_income


def assessed_income_HCP(W_):
    TSI1 = 5304
    beta_i = 60400
    I_hat = max(calculate_pension_income(W_) + 0.0025 * W_ + 0.02*max(W_ - beta_i, 0) - TSI1, 0)
    return I_hat


def BDF_HCP(lvl):
    if lvl == 1:
        return 4172
    if lvl == 2:
        return 4409
    if lvl == 3:
        return 4533
    if lvl == 4:
        return 4654


def Gstar_HCP(lvl):
    if lvl == 1:
        return 10271
    if lvl == 2:
        return 18064
    if lvl == 3:
        return 39311
    if lvl == 4:
        return 59594


def Fm_HCP(W_, lvl):
    I_1_HCP = 32820
    I_2_HCP = 46143
    I_3_HCP = 63352
    I_4_HCP = 76675
    F_1_HCP = 6662
    F_2_HCP = 13324
    I_hat = assessed_income_HCP(W_)
    if I_hat <= I_1_HCP:
        return 0
    # Case 2: If the estimated index is between the first and second thresholds
    if I_1_HCP < I_hat <= I_2_HCP:
        return 0.5 * (I_hat - I_1_HCP)
    # Case 3: If the estimated index is between the second and third thresholds
    if I_2_HCP < I_hat <= I_3_HCP:
        return F_1_HCP
    # Case 4: If the estimated index is between the third and fourth thresholds
    if I_3_HCP < I_hat <= I_4_HCP:
        return F_1_HCP + 0.5 * (I_hat - I_3_HCP)
    # Case 5: If the estimated index exceeds the fourth threshold
    if I_hat > I_4_HCP:
        return F_2_HCP


def F_HCP(W_, lvl):
    BDF = BDF_HCP(lvl)
    return BDF + Fm_HCP(W_, lvl)


def GRandF_HCP(W_, LEVEL):
    w1 = 0.07
    w2 = 0.53
    w3 = 0.4
    if LEVEL == 'medium':
        F_HCP_avg = w1*F_HCP(W_, 1)+w2*F_HCP(W_, 2)+w3*F_HCP(W_, 3)
        GR_HCP_avg = w1*Gstar_HCP(1) + w2*Gstar_HCP(2) + w3*Gstar_HCP(3) + calculate_pension_income(W_) - F_HCP_avg 
        return GR_HCP_avg, F_HCP_avg
    if LEVEL == 'high':
        return Gstar_HCP(4) + calculate_pension_income(W_) - F_HCP(W_, 4), F_HCP(W_, 4)
