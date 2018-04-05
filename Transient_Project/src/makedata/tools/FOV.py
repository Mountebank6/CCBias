"""
Apply Field of Vision to true data


"""


__author__ = "Theo Faridani"

import numpy as np
import math
import astropy.nddata as nd

def write_circle_fov(dattype, data, radius, loc, output_filename):
    shape = data.shape
    final = np.zeros(shape, dtype=dattype)
    for i in range(shape[0]):
        for k in range(shape[1]):
            if math.hypot(i-loc[0], k-loc[1]) <= radius:
                final[(i,k)] = data[(i,k)]
    
    #this is really inefficient, but it's at least consistent
    wrap = nd.CCDData(final, unit='adu')
    wrap.write(output_filename + ".fits")

def apply_circle_fov(imagearray, radius, loc):
    """Return an imagearray with all but a circle turned to black
    
    imagearray must be a numpy array"""
    shape = imagearray.shape
    final = np.zeros(shape, dtype=imagearray.dtype)
    loweri = max(0,loc[0]-radius)
    upperi = min(shape[0],loc[0]+radius)
    lowerk = max(0,loc[1]-radius)
    upperk = min(shape[1],loc[1]+radius)
    
    for i in range(loweri, upperi):
        for k in range(lowerk, upperk):
            if math.hypot(i-loc[0], k-loc[1]) <= radius:
                final[i][k] = imagearray[i][k]
    return final

def write_rectagle_fov(dattype, data, rect, ulc, output_filename):
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
    
def apply_dynamic_random_scatter(dattype, data, fraction):
    if fraction < 0  or fraction > 1:
        raise ValueError("fraction is not between 0 and 1")
    shape = data.shape
    final = np.zeros(shape, dtype=dattype)
    for i in range(len(final)):
        for k in range(len(final[i])):
            if np.random.rand() < fraction:
                final[i][k] = 0
    return final

def make_static_cover(shape, fraction):
    if fraction < 0  or fraction > 1:
        raise ValueError("fraction is not between 0 and 1")
    badlist = []
    stupid = np.zeros(shape, dtype=np.uint8)
    for i in range(len(stupid)):
        for k in range(len(stupid[i])):
            if np.random.rand() < fraction:
                badlist.append((i,k))
    return badlist

def apply_static_random_scatter(data, cover):
    for i in range(data):
        for k in range(data[i]):
            if (i,k) in cover:
                data[i][k] = 0*data[i][k]
    return data
    
def apply_dynamic_img_scatter(data, fraction):
    if fraction < 0  or fraction > 1:
        raise ValueError("fraction is not between 0 and 1")    
    for i in range(len(data)):
        for k in range(len(data[i])):
            if np.random.rand() < fraction:
                data[i][k] = 0*data[i][k]
    return data