"""
Library of Performance Functions for use by the optimizers

"""

import numpy as np

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
