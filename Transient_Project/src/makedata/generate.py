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
        self.current_remaining_life = []
        for i in range(len(self.astro_data.data)):
            for k in range(len(self.astro_data.data[i])):
                if np.random.rand() < self.rate:
                    if self.lifetime_sigma is not None:
                        lifetime = np.random.normal(self.lifetime,
                                             self.lifetime_sigma)
                    else:
                        lifetime = self.lifetime
                    birth = np.random.uniform(-lifetime,0)
                    self.current_event_births.append(birth)
                    self.current_event_locations.append((i,k))
                    self.current_remaining_life.append(0.0 - birth)
                        
    
    def set_intensity_guassian(self,mag,sigma):
        """Give new events gaussian intensity"""
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
        self.gauss_intensity = gauss_intensity
        self.gauss_sigma = gauss_sigma
        self.astro_data = nd.NDDataRef(np.zeros(self.shape, self.data_type))
        
        if self.shape is None:
            raise TypeError("Required argument 'shape' (pos 1) not found")
        if self.delta_t is None:
            raise TypeError("Required argument 'delta_t' (pos 2) not found")
        
        check_shape(self.shape)
        check_data_type(self.data_type)
        check_delta_t(self.delta_t)
        check_rate(self.rate)
        check_n(self.n)
        check_lifetime_sigma(self.lifetime_sigma)
        check_gauss_intensity(self.gauss_intensity)
        check_gauss_sigma(self.gauss_sigma)
#TODO: Current code throws errors if some values are at their default
#    of none. Make sure this is really what you want.
        self.new_population()
        if (gauss_intensity is not None) and (gauss_sigma is not None):
            self.set_intensity_guassian(gauss_intensity, gauss_sigma)
    
def check_shape(shape):
    """Throw errors if types/values are wrong"""
    if not isinstance(shape, tuple):
        raise TypeError("Bad operand type for shape: " 
                        + str(type(shape)))
    if len(shape) != 2:
        raise ValueError("shape is not of length 2")
    for x in shape:
        if not isinstance(x, int):
            raise TypeError("shape tuple must contain ints")
    
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
    if delta_t <= 0:
        raise ValueError("delta_t must be >0")
        
def check_rate(rate):
    """Throw errors if types/values are wrong"""
    if not (isinstance(rate, float)
            or isinstance(rate, np.ndarray)):
        raise TypeError("Bad operand type for rate: "
                        + str(type(rate)) + "\n Must be" 
                        + " float or numpy array of same shape as shape")
    if isinstance(rate, float):
        if rate > 1 or rate < 0:
            raise ValueError("rate is not a probability. " + 
                             "Must be between 0 and 1 inclusive")
def check_n(n):
    """Throw errors if types/values are wrong"""
    if n is not None:
        if not isinstance(n, int):
            raise TypeError("Bad operand type for n: "
                            + str(type(n)) + "\n Must be int") 
        if n < 1:
            raise ValueError("n must be >= 1")

def check_lifetime_sigma(lifesigma):
    """Throw errors if types/values are wrong"""
    if lifesigma is not None:
        if not isinstance(lifesigma, float):
            raise TypeError("Bad operand type for lifetime_sigma: "
                            + str(type(lifesigma))) + "\n Must be float"
        if lifesigma <= 0:
            raise ValueError("Sigma of event lifetime is <= 0. Bad!")

def check_gauss_intensity(inten):
    """Throw errors if types/values are wrong"""
    if inten is not None:
        if not isinstance(inten, float):
            raise TypeError("Bad operand type for gauss_intensity: "
                            + str(type(inten))) + "\n Must be float"
        if inten < 0:
            raise ValueError("Intensity must be >= 0")

def check_gauss_sigma(sigm):
    """Throw errors if types/values are wrong"""
    if sigm is not None:
        if not isinstance(sigm, float):
            raise TypeError("Bad operand type for gauss_sigma: "
                            + str(type(sigm))) + "\n Must be float"
        if sigm <= 0:
            raise ValueError("Sigma of event intensity is <= 0. Bad!")
                                