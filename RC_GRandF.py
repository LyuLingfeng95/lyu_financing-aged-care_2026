from age_pension import calculate_pension_income


def assessed_assets_RC(W_, H_):
    H_RC = 201230
    extra_W = min(H_, H_RC)
    W_hat = W_ + extra_W
    return W_hat


def assessed_income_RC(W_, H_, Leasing):
    TSI1 = 5304
    beta_i = 60400
    if Leasing == 1:
        return max(calculate_pension_income(W_, 0.04*H_) + 0.04*H_ + 0.0025 * W_ + 0.02*max(W_ - beta_i, 0) - TSI1, 0)
    if Leasing == 0:
        return max(calculate_pension_income(W_) + 0.0025 * W_ + 0.02*max(W_ - beta_i, 0) - TSI1, 0)


def real_income_RC(W_, H_, Leasing):
    if Leasing == 1:
        return calculate_pension_income(W_, 0.04*H_) + 0.04*H_
    if Leasing == 0:
        return calculate_pension_income(W_)


def means_RC(W_, H_, Leasing):
    I_hat = assessed_income_RC(W_, H_, Leasing)
    W_hat = assessed_assets_RC(W_, H_)
    I_RC_t = [32820, 81566]
    W_RC_t = [59500, 201230, 484697]
    I1 = I_RC_t[0]
    W1, W2, W3 = W_RC_t[0], W_RC_t[1], W_RC_t[2]
    if W_hat < W1:
        return max(0.5 * (I_hat-I1), 0)
    if W1 <= W_hat < W2:
        return max(0.5 * (I_hat-I1), 0) - 0.175 * W1 + 0.175 * W_hat
    if W2 <= W_hat < W3:
        return max(0.5 * (I_hat-I1), 0) - 0.175 * W1 + 0.165 * W2 + 0.01 * W_hat
    if W3 <= W_hat:
        return max(0.5 * (I_hat-I1), 0) - 0.175 * W1 + 0.165 * W2 - 0.01 * W3 + 0.02 * W_hat


def total_fee_RC(W_, H_, Leasing):
    cap_annual = 33309
    BDF = 4656
    AC_m = means_RC(W_, H_, Leasing)
    tp1 = BDF + AC_m
    tp2 = 0
    if AC_m >= 24871:
        tp2 = tp2 + max(0,  0.04 * H_ - 24871)
    return min(tp1 + tp2, cap_annual)


def GRandF_RC(W_, H_, Leasing):
    G_star = 59594
    return G_star + real_income_RC(W_, H_, Leasing) - total_fee_RC(W_, H_, Leasing), total_fee_RC(W_, H_, Leasing)