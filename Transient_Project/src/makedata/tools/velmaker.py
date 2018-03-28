"""
Generate random velocities projected onto the sky

"""

import numpy as np
import math

__all__ = ['get_velocity']

vels = []
for i in range(100000):
    x = np.random.rand()
    y = np.random.rand()
    z = np.random.rand()
    mag = math.sqrt(x**2+y**2+z**2)
    x = x/mag
    y = y/mag
    z = z/mag
    vels.append(np.asanyarray([y,x]))
    #choose y before x to mimic matrix-style notation

def get_unifv():
    """Return a random element of the uniform velocity distribution"""
    return vels[np.random.randint(0,100000)]