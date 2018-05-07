"""
Library of Performance Functions for use by the optimizers

There is a pseudo-standardized argument priority for the scoring functions
that give scores independent of the past (i.e. depend only on
the current data being fed into it). Arguments with lower priority
are fed in earlier:
    Argument Priority:
        1- The generator to draw from (e.g. a TransientSeries object)
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

def int_intensity_circle(generator, rowloc, columnloc, radius):
    """Return number of events visisble inside a set circle"""
    
    shape = generator.get_shape()
    #i is for row, k is for column
    #maps to [0] and [1] in the location tuple/list
    loweri = max(0,rowloc-radius)
    upperi = min(shape[0],rowloc+radius)
    lowerk = max(0,columnloc-radius)
    upperk = min(shape[1],columnloc+radius)

    score = 0

    for loc in generator.get_cur_locs():
        if (loc[0] - rowloc)**2 + (loc[1] - columnloc)**2 <= radius:
            if loc[0] <= upperi and loc[0] >= loweri:
                if loc[1] <= upperk and loc[1] >= lowerk:
                    score += 1
    return score

def int_intensity_square(generator, rowloc, columnloc, radius):
    """Return number of events visisble inside a set circle"""
    
    shape = generator.get_shape()
    #i is for row, k is for column
    #maps to [0] and [1] in the location tuple/list
    loweri = max(0,rowloc-radius)
    upperi = min(shape[0],rowloc+radius)
    lowerk = max(0,columnloc-radius)
    upperk = min(shape[1],columnloc+radius)

    data = generator.get_astro_data_data()
    score = np.sum(data[loweri:upperi][lowerk:upperk]>0)
    return score
