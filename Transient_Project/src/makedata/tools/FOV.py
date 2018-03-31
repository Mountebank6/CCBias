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
                data[(i,k)] = 0
    return data
    
def apply_dynamic_img_scatter(data, fraction):
    if fraction < 0  or fraction > 1:
        raise ValueError("fraction is not between 0 and 1")    
    for i in range(len(data)):
        for k in range(len(data[i])):
            if np.random.rand() < fraction:
                brt = data[i][k]
                data[i][k] = [0,0,0,0]
    return data