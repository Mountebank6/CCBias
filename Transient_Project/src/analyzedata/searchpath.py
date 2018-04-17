"""
Set of tools for characterizing optimal search path

"""

import numpy as np
import cmath

def path_as_fft(locations, n=None):
    """Parametrize the search path as an fft
    
    Counter to intuition, the "x-axis" of the array 
    (left/right) is the imaginary axis since
    we are using matrix notation (i.e. NxM matrix
    has N rows and M columns)
    """
    z = []
    for location in locations:
        z.append(location[0] + location[1]*1j)
    return np.fft.fft(z, n)