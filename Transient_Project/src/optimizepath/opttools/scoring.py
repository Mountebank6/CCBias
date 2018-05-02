"""
Library of Performance Functions for use by the optimizers

"""

import numpy as np
import math

def int_intensity(data):
    """Return the number of events visisble in a snapshot

    data: a 2D intensity numpy array

    Look through the elements of the array. For each element
    that is not equal to the zero element, add 1 to the score
    """
    score = 0
    for row in data:
        if (np.zeros_like(row) != row).all():
            for element in row:
                if (np.zeros_like(element) != element).all():
                    score += 1
    return score

def int_intensity_circle(data, radius, loc):
    """Return number of events visisble inside a set circle"""
    
    shape = data.shape
    loweri = max(0,loc[0]-radius)
    upperi = min(shape[0],loc[0]+radius)
    lowerk = max(0,loc[1]-radius)
    upperk = min(shape[1],loc[1]+radius)

    score = 0

    for i in range(loweri, upperi):
        for k in range(lowerk, upperk):
            if math.hypot(i-loc[0], k-loc[1]) <= radius:
                if data[i][k] != np.zeros_like(data[i][k]):
                    score += 1
    return score