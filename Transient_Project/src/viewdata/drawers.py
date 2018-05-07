"""Functions to draw results

"""
import numpy as np
from scipy import integrate
from math import sqrt, pi, exp

#Most of this is garbage, but I needed a place to store is
number = 500
shap = (500,500)
mean = 10
sigm = 5
dt = 1
velo = 0
prob = 0.0000002

def fakenorm(x):
    return 1/sqrt(2*pi*sigm**2)*exp(-(x-mean)**2/(2*sigm**2))

modifier = 1/(integrate.quad(fakenorm,0,np.inf)[0])

def firstmoment(x):
    return modifier*x/sqrt(2*pi*sigm**2)*exp(-(x-mean)**2/(2*sigm**2))
def secondmoment(x):
    return modifier*x**2/sqrt(2*pi*sigm**2)*exp(-(x-mean)**2/(2*sigm**2))

truemean = integrate.quad(firstmoment,0,np.inf)[0]
truesigm = sqrt(integrate.quad(secondmoment,0,np.inf)[0] - truemean**2)


def make_greens_array(transseries):
    final = np.zeros((shap[0],shap[1],4), dtype=np.uint8)
    for i in range(len(transseries.get_cur_locs())):
        if (transseries.get_cur_locs()[i][0] in range(shap[0]) 
                and transseries.get_cur_locs()[i][1] in range(shap[1])):
            loc = transseries.get_cur_locs()[i]
            lt = (transseries.get_cur_durations()[i] 
                + transseries.get_current_time() 
                - transseries.get_cur_births()[i])
            if lt > truemean + truesigm:
                final[loc[0]][loc[1]] = [0,255,0,255]
            else:
                final[loc[0]][loc[1]] = [255,255,255,255]
    return final

def make_bluegreens_array(transseries):
    final = np.zeros((shap[0],shap[1],4), dtype=np.uint8)
    for i in range(len(transseries.get_cur_locs())):
        if (transseries.get_cur_locs()[i][0] in range(shap[0]) 
                and transseries.get_cur_locs()[i][1] in range(shap[1])):
            loc = transseries.get_cur_locs()[i]
            lt = (transseries.get_cur_durations()[i] 
                + transseries.get_current_time() 
                - transseries.get_cur_births()[i])
            if lt > truemean + truesigm:
                final[loc[0]][loc[1]] = [0,255,0,255]
            elif lt > truemean and lt < truemean + truesigm:
                final[loc[0]][loc[1]] = [255,0,0,255]
            else:
                final[loc[0]][loc[1]] = [255,255,255,255]
    return final




