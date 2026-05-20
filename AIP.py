import numpy as np

# def xiatt(t, alpha, I_RACF):
#     T = 40
#     if I_RACF == 0:
#         return ((0.5*t+T)/T) * alpha/(1+alpha)
#     if I_RACF == 1:
#         return alpha/(1+alpha)


def Hstate2IRACF(Hstate):
    if Hstate == 5:
        return 1
    if Hstate != 5:
        return 0 

def xiatt(t, alpha, I_RACF):
    T = 40
    kappa = 9/5
    chi = (np.log(1/kappa)/(-40))
    if I_RACF == 0:
        return kappa * np.exp(chi*(t-T)) * alpha/(1+alpha)
    if I_RACF == 1:
        return alpha/(1+alpha)
