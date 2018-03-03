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

class TransientSeries:
    """Handle creation and iteration of image set
    """
    
    
    def new_population(self):
        """Generate fresh transient population and clear old one"""
        self.current_event_locations = []
        self.current_event_births = []
        self.current_lifetimes = []
        if isinstance(self.rate, float):
            if self.rate <= 1 and self.rate >= 0:
                for i in range(len(self.astro_data.data)):
                    for k in range(len(self.astro_data.data[i])):
                        if np.random.rand() < self.rate:
                            self.current_event_births.append(0.0)
                            self.current_event_locations.append((i,k))
                            self.current_lifetimes.append(
                                np.random.normal(self.lifetime,
                                                 self.lifetime_sigma))
    
    def set_intensity_guassian(self,mag,sigma):
        """Give new events guassian intensity"""
        for index in self.current_event_locations:
            if self.astro_data.data[index] == 0:
                self.astro_data.data[index] = np.random.normal(mag,sigma)
        
    def __init__(self, shape=None, delta_t=None,
                 n=None, rate=None, lifetime=None, 
                 lifetime_sigma=1e-100, data_type=np.uint16,
                 gauss_intensity=None, gauss_sigma=None):
        """Generate initial conditions from parameters.
        """
        
        self.shape = shape
        self.n = n
        self.delta_t = delta_t
        self.rate = rate
        self.data_type = data_type
        self.lifetime = lifetime
        self.lifetime_sigma = lifetime_sigma
        self.astro_data = nd.NDDataRef(np.zeros(self.shape, 
                                                dtype=self.data_type))
        
        if self.shape is None:
            raise TypeError("Required argument 'shape' (pos 1) not found")
        if self.delta_t is None:
            raise TypeError("Required argument 'delta_t' (pos 2) not found")
        
        check_shape(self.shape)
        check_data_type(self.data_type)
        check_delta_t(self.delta_t)
        check_rate(self.rate)
        check_n(self.n)
        check_lifetime_sigma(lifetime_sigma)
        #TODO: CHECK INTENSITY AND SIGMA
        self.new_population()
        if (gauss_intensity is not None) and (gauss_sigma is not None):
            self.set_intensity_guassian(gauss_intensity, gauss_sigma)
        #TODO: write better code
    
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
        
def check_rate(rate):
    """Throw errors if types/values are wrong"""
    if not (isinstance(rate, float)
            or isinstance(rate, np.ndarray)):
        raise TypeError("Bad operand type for rate: "
                        + str(type(rate)) + "\n Must be" 
                        + " float or numpy array of same shape as shape")
def check_n(n):
    """Throw errors if types/values are wrong"""
    if not isinstance(n, int):
        raise TypeError("Bad operand type for n: "
                        + str(type(n)) + "\n Must be int") 

def check_lifetime_sigma(lifesigma):
    if not isinstance(lifesigma, float):
        raise TypeError("Bad operand type for lifetime_sigma: "
                        + str(type(lifesigma))) + "\n Must be float"
        
        