"""
Apply Field of Vision to true data


"""


__author__ = "Theo Faridani"

import numpy as np
import math
import astropy.nddata as nd

def write_circle_fov(dattype, data, radius, loc, output_filename):
    """Apply a circle fov and write a fits image"""
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

def apply_square_fov(imagearray, radius, loc):
    """Return an imagearray with all but a square turned to black
    
    imagearray must be a numpy array"""
    shape = imagearray.shape
    final = np.zeros(shape, dtype=imagearray.dtype)
    lowi = max(0,loc[0]-radius)
    upi = min(shape[0],loc[0]+radius)
    lowk = max(0,loc[1]-radius)
    upk = min(shape[1],loc[1]+radius)

    final[lowi:upi,lowk:upk] = imagearray[lowi:upi,lowk:upk]


    return final


def write_rectagle_fov(dattype, data, rect, ulc, output_filename):
    """Apply a rectangle fov and write the result
    
    Using matrix notation for indeces, take the upper-left-corner
    and extend it down by rect[0] and right by rect[1]
    then write the result
    
    Arguments:
    dattype:
        data type of numpy array
    data:
        numpy array to add fov to
    rect:
        length 2 iterable. form (down, right) determines how
        far down and right from the upper left corner the rectangle extends
    ulc:
        length 2 iterable. matrix location of the upper left corner of the
        rectangle
    output_filename:
        filename to write to. the '.fits' is added automatically
    """
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
    
def apply_dynamic_random_scatter(dattype, data, covered_fraction):
    """cover a random fraction of the data"""
    if covered_fraction < 0  or covered_fraction > 1:
        raise ValueError("covered_fraction is not between 0 and 1")
    shape = data.shape
    final = np.zeros(shape, dtype=dattype)
    for i in range(len(final)):
        for k in range(len(final[i])):
            if np.random.rand() > covered_fraction:
                final[i][k] = data[i][k]
    return final

def make_static_cover(shape, covered_fraction):
    """make a list of random indeces to cover"""
    if covered_fraction < 0  or covered_fraction > 1:
        raise ValueError("fraction is not between 0 and 1")
    badlist = []
    stupid = np.zeros(shape, dtype=np.uint8)
    for i in range(len(stupid)):
        for k in range(len(stupid[i])):
            if np.random.rand() < covered_fraction:
                badlist.append((i,k))
    return badlist

def apply_static_random_scatter(data, cover):
    """Darken the listed indeces"""
    final = np.zeros(data.shape, data.dtype)
    for i in range(data):
        for k in range(data[i]):
            if (i,k) not in cover:
                final[i][k] = data[i][k]
    return final
    
def apply_dynamic_img_scatter(data, covered_fraction):
    """Pick a fraction of points at random and darken them"""
    final = np.zeros(data.shape, data.dtype)
    if covered_fraction < 0  or covered_fraction > 1:
        raise ValueError("fraction is not between 0 and 1")    
    for i in range(len(data)):
        for k in range(len(data[i])):
            if np.random.rand() > covered_fraction:
                final[i][k] = data[i][k]
    return data