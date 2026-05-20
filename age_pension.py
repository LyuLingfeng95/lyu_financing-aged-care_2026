def calculate_pension_income(W_t, Rental_Income=0):
    TSI1 = 5304
    TSI2 = 63351
    beta_i = 60400
    alpha_1 = 301750
    alpha_2 = 674000
    MPR = 1020
    means_income_t = MPR/(TSI2 - TSI1) * (max(0.0025 * W_t + 0.02*max(W_t-beta_i, 0) + Rental_Income -TSI1, 0))
    means_assets_t = MPR / (alpha_2 - alpha_1) * (max(W_t - alpha_1, 0))
    I_t = max(MPR - max(means_income_t, means_assets_t), 0) * 26
    return I_t


