"""
Generate fake sample data for testing.


"""

from __future__ import division
from blaze.expr.expressions import shape

__author__ = "Theo Faridani"
__version__ = "0.08"

import numpy as np
import astropy.nddata as nd

_allowed_types = [np.uint8, np.uint16, np.uint32, np.uint64,
                 np.float16, np.float32, np.float64]

def check_shape(shape):
    """Check shape's types and value"""
    if not isinstance(shape, tuple):
        raise TypeError("Bad operand type for shape: " 
                        + str(type(shape)))
    if len(shape) != 2:
        raise ValueError("shape is not of length 2")
    
def check_data_type(data_type):
    """Check data_type's types and value"""
    if data_type not in _allowed_types:
        raise TypeError("Bad operand type for data_type: " 
                        + str(type(data_type)) + "\n Must be"
                        + "one of " + str(_allowed_types))
            
def check_delta_t(delta_t):
    """Check delta_t's types and value"""
    if not (isinstance(delta_t, float) 
            or isinstance(delta_t, int)):
        raise TypeError("Bad operand type for delta_t: " + str(type(delta_t))
                        + "\n Must be a python float or python int")
        
def check_event_rate(event_rate):
    """Check event_rate's types and value"""
    if not (isinstance(event_rate, float)
            or isinstance(event_rate, np.ndarray)):
        raise TypeError("Bad operand type for event_rate: "
                        + str(type(event_rate)) + "\n Must be" 
                        + " float or numpy array of same shape as shape")
def check_n(n):
    """Check n's types and value"""
    if not isinstance(n, int):
        raise TypeError("Bad operand type for n: "
                        + str(type(n)) + "\n Must be int")


class TransientSeries:
    """Handle creation and iteration of image set
    """
    
    
    def new_population(self, shape, event_rate, event_lifetime, data_type):
        """Generate fresh transient population and clear old one"""
        blank_image = nd.NDDataRef(np.zeros(shape, dtype=data_type))
   
    def __init__(self, shape=None, delta_t=None,
                 n=None, event_rate=None, event_lifetime=None,
                 data_type=np.uint16):
        """Generate initial conditions from parameters.
        """
        
        self.shape = shape
        self.n = n
        self.delta_t = delta_t
        self.event_rate = event_rate
        self.data_type = data_type
        self.event_lifetime = event_lifetime
        
        if self.shape is None:
            raise TypeError("Required argument 'shape' (pos 1) not found")
        if self.delta_t is None:
            raise TypeError("Required argument 'delta_t' (pos 2) not found")
        
        check_shape(self.shape)
        check_data_type(self.data_type)
        check_delta_t(self.delta_t)
        check_event_rate(self.event_rate)
        check_n(self.n)
        
        self.image = nd.NDDataRef(np.zeros(shape, dtype=self.data_type))
        
        
        
        