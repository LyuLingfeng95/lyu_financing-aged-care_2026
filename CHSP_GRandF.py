from age_pension import calculate_pension_income

def GRandF_CHSP(W_):
    GR = 3475 - 270 + calculate_pension_income(W_)
    F = 270
    return GR, F