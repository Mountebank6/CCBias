"""
Library of Performance Functions for use by the optimizers

There is a pseudo-standardized argument priority for the scoring functions
that give scores independent of the past (i.e. depend only on
the current data being fed into it). Arguments with lower priority
are fed in earlier:
    Argument Priority:
        1- The data to be scored. (Not a part of any genome)
        2- Row location around which to score
        3- Column location around which to score
        4- A lengthscale to detirmine how much area to score
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

def int_intensity_circle(data, rowloc, columnloc, radius):
    """Return number of events visisble inside a set circle"""
    
    shape = data.shape
    loweri = max(0,rowloc-radius)
    upperi = min(shape[0],rowloc+radius)
    lowerk = max(0,columnloc-radius)
    upperk = min(shape[1],columnloc+radius)

    score = 0

    for i in range(loweri, upperi):
        for k in range(lowerk, upperk):
            if math.hypot(i-rowloc, k-columnloc) <= radius:
                if data[i][k] != np.zeros_like(data[i][k]):
                    score += 1
    return score