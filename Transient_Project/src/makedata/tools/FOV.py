"""
Apply Field of Vision to true data


"""


__author__ = "Theo Faridani"

import numpy as np
import math
import astropy.nddata as nd

def apply_circle_fov(dattype, data, radius, loc, output_filename):
    shape = data.shape
    final = np.zeros(shape, dtype=dattype)
    for i in range(shape[0]):
        for k in range(shape[1]):
            if math.hypot(i-loc[0], k-loc[1]) <= radius:
                final[(i,k)] = data[(i,k)]
    
    #this is really inefficient, but it's at least consistent
    wrap = nd.CCDData(final, unit='adu')
    wrap.write(output_filename + ".fits")

def apply_rectagle_fov(dattype, data, rect, ulc, output_filename):
    #ulc stands for upper left corner
    shape = data.shape
    final = np.zeros(shape, dtype=dattype)
    for i in range(shape[0]):
        for k in range(shape[1]):
            if ((i - ulc[0]) <= rect[0] and (k - ulc[1]) <= rect[1]):
                final[(i,k)] = data[(i,k)]
            
    #this is really inefficient, but it's at least consistent
    wrap = nd.CCDData(final, unit='adu')
    wrap.write(output_filename + ".fits")