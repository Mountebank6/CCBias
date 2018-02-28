"""
Generate fake sample data for testing.


"""

__author__ = "Theo Faridani"
__version__ = "0.1"

import numpy as np
import astropy.nddata as nd

allowed_types = [np.uint8, np.uint16, np.uint32, np.uint64,
                 np.float16, np.float32, np.float64]

__all__ = ['populate']

def populate(shape = None, datatype = None):
    """Return initial conditions and properties of event sample
    """
    if shape is None:
        raise TypeError("You must give a shape")
    if type(shape) != type(tuple):
        raise TypeError("bad operand type for shape: " 
                        + str(type(shape)))
    if datatype is None:
        raise TypeError("You must give a data type")
    if datatype not in allowed_types:
        raise TypeError("datatype is of incorrect type. " +
                        "must be one of " + str(allowed_types))
    
    initial_image = nd.NDData(np.zeros(shape, dtype=datatype))

    return [initial_image]
