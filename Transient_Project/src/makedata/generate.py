"""
Generate fake sample data for testing.


"""

from __future__ import division

__author__ = "Theo Faridani"
__version__ = "0.08"

import numpy as np
import astropy.nddata as nd

_allowed_types = [np.uint8, np.uint16, np.uint32, np.uint64,
                 np.float16, np.float32, np.float64]

class TransientSeries:
    """Handle creation and iteration of image set
    """
    
    
    def __init__(self, shape=None, deltat=None,
                 n=None, eventrate=None, datatype=np.uint16):
        """Generate initial conditions from parameters.
        """
        
        self.shape = shape
        self.n = n
        self.deltat = deltat
        self.eventrate = eventrate
        self.datatype = datatype
        
        if self.shape is None:
            raise TypeError("Required argument 'shape' (pos 1) not found")
        if self.deltat is None:
            raise TypeError("Required argument 'deltat' (pos 2) not found")
        
        if not isinstance(self.shape, tuple):
            raise TypeError("Bad operand type for shape: " 
                            + str(type(self.shape)))
        if len(self.shape) != 2:
            raise ValueError("shape is not of length 2")
        if self.datatype not in _allowed_types:
            raise TypeError("Bad operand type for shape: " 
                            + str(type(self.datatype)) + "\n Must be"
                            + "one of " + str(_allowed_types))
        self.image = nd.NDData(np.zeros(shape, dtype=self.datatype))
        
        if not (isinstance(self.deltat, float) 
                or isinstance(self.deltat, int)):
            raise TypeError("deltat should be a python float or python int")
        
        