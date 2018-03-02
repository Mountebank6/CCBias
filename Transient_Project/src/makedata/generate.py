"""
Generate fake sample data for testing.


"""

from __future__ import division

__author__ = "Theo Faridani"
__version__ = "0.09"

import numpy as np
import astropy.nddata as nd

_allowed_types = [np.uint8, np.uint16, np.uint32, np.uint64,
                 np.float16, np.float32, np.float64]

def check_shape(shape):
    """Throw errors if types/values are wrong"""
    if not isinstance(shape, tuple):
        raise TypeError("Bad operand type for shape: " 
                        + str(type(shape)))
    if len(shape) != 2:
        raise ValueError("shape is not of length 2")
    
def check_data_type(data_type):
    """Throw errors if types/values are wrong"""
    if data_type not in _allowed_types:
        raise TypeError("Bad operand type for data_type: " 
                        + str(type(data_type)) + "\n Must be"
                        + "one of " + str(_allowed_types))
            
def check_delta_t(delta_t):
    """Throw errors if types/values are wrong"""
    if not (isinstance(delta_t, float) 
            or isinstance(delta_t, int)):
        raise TypeError("Bad operand type for delta_t: " + str(type(delta_t))
                        + "\n Must be a python float or python int")
        
def check_event_rate(event_rate):
    """Throw errors if types/values are wrong"""
    if not (isinstance(event_rate, float)
            or isinstance(event_rate, np.ndarray)):
        raise TypeError("Bad operand type for event_rate: "
                        + str(type(event_rate)) + "\n Must be" 
                        + " float or numpy array of same shape as shape")
def check_n(n):
    """Throw errors if types/values are wrong"""
    if not isinstance(n, int):
        raise TypeError("Bad operand type for n: "
                        + str(type(n)) + "\n Must be int")


class TransientSeries:
    """Handle creation and iteration of image set
    """
    
    
    def new_population(self):
        """Generate fresh transient population and clear old one"""
        blank_image = nd.NDDataRef(np.zeros(self.shape, dtype=self.data_type))
        self.current_event_locations = []
        self.current_event_births = []
        self.current_event_lifetimes = []
        if isinstance(self.event_rate, float):
            if self.event_rate <= 1 and self.event_rate >= 0:
                for i in range(len(blank_image.data)):
                    for k in range(len(blank_image.data[i])):
                        if np.random.rand() < self.event_rate:
                            self.current_event_births.append(0.0)
                            self.current_event_locations.append((i,k))
                            self.current_event_lifetimes.append(
                                np.random.normal(self.event_lifetime,
                                                 self.event_lifetime_sigma))
        
    def __init__(self, shape=None, delta_t=None,
                 n=None, event_rate=None, event_lifetime=None, 
                 event_lifetime_sigma=1e-100, data_type=np.uint16):
        """Generate initial conditions from parameters.
        """
        
        self.shape = shape
        self.n = n
        self.delta_t = delta_t
        self.event_rate = event_rate
        self.data_type = data_type
        self.event_lifetime = event_lifetime
        self.event_lifetime_sigma = event_lifetime_sigma
        
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
        
        
        
        