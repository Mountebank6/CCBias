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
    
    
    def __init__(self, shape=None, delta_t=None,
                 n=None, rate=None, lifetime=None, 
                 lifetime_sigma=None, data_type=np.uint16,
                 gauss_intensity=None, gauss_sigma=None):
        """Generate initial conditions from parameters.
        """
        
        self.shape = shape
        self.n = n
        self.delta_t = delta_t
        self.rate = rate
        self.data_type = data_type
        self.lifetime = float(lifetime)
        self.lifetime_sigma = float(lifetime_sigma)
        self.gauss_intensity = float(gauss_intensity)
        self.gauss_sigma = float(gauss_sigma)
        self.astro_data = nd.NDDataRef(np.zeros(self.shape, self.data_type))
        
        if self.shape is None:
            raise TypeError("Required argument 'shape' (pos 1) not found")
        if self.delta_t is None:
            raise TypeError("Required argument 'delta_t' (pos 2) not found")
        
        self.check_shape()
        self.check_data_type()
        self.check_delta_t()
        self.check_rate()
        self.check_n()
        self.check_lifetime()
        self.check_lifetime_sigma()
        self.check_gauss_intensity()
        self.check_gauss_sigma()
#TODO: Current code throws errors if some values are at their default
#    of none. Make sure this is really what you want.
        self.new_population()
        if (
                self.gauss_intensity is not None 
                and self.gauss_sigma is not None):
            self.set_intensity_guassian(gauss_intensity, gauss_sigma)
    
    def new_population(self):
        """Generate fresh transient population and clear old one
        
        Iterate through the array, 
        """
        self.current_event_locations = []
        self.current_event_births = []
        self.current_remaining_life = []
        if isinstance(self.rate, float):
            for i in xrange(len(self.astro_data.data)):
                for k in xrange(len(self.astro_data.data[i])):   
                    if np.random.rand() < self.rate:
                        if self.lifetime_sigma is not None:
                            lifetime = np.random.normal(
                                                self.lifetime,
                                                self.lifetime_sigma)
                        else:
                            lifetime = self.lifetime
                        birth = np.random.uniform(-lifetime,0)
                        self.current_event_births.append(birth)
                        self.current_event_locations.append((i,k))
                        self.current_remaining_life.append(0.0 - birth)
                        
        if isinstance(self.rate, np.ndarray):
            if len(self.rate.shape) == 2:
                for i in xrange(len(self.astro_data.data)):
                    for k in xrange(len(self.astro_data.data)):
                        if np.random.rand() < self.rate[i][k]:
                            if self.lifetime_sigma is not None:
                                lifetime = np.random.normal(
                                                    self.lifetime,
                                                    self.lifetime_sigma)
                            else:
                                lifetime = self.lifetime
                            birth = np.random.uniform(-lifetime,0)
                            self.current_event_births.append(birth)
                            self.current_event_locations.append((i,k))
                            self.current_remaining_life.append(0.0 - birth)
            else:
                for i in xrange(len(self.astro_data.data)):
                    for k in xrange(len(self.astro_data.data)):
                        if np.random.rand() < self.rate[0][i][k]:
                            if self.lifetime_sigma is not None:
                                lifetime = np.random.normal(
                                                    self.lifetime,
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
    
    def check_shape(self):
        """Throw errors if types/values are wrong"""
        if not isinstance(self.shape, tuple):
            raise TypeError("Bad operand type for shape: " 
                            + str(type(self.shape)))
        if len(self.shape) != 2:
            raise ValueError("shape is not of length 2")
        for x in self.shape:
            if not isinstance(x, int):
                raise TypeError("shape tuple must contain ints")
        
    def check_data_type(self):
        """Throw errors if types/values are wrong"""
        if self.data_type not in _allowed_types:
            raise TypeError("Bad operand type for data_type: " 
                            + str(type(self.data_type)) + "\n Must be"
                            + "one of " + str(_allowed_types))
                
    def check_delta_t(self):
        """Throw errors if types/values are wrong"""
        if not (isinstance(self.delta_t, float) 
                or isinstance(self.delta_t, int)):
            raise TypeError("Bad operand type for delta_t: " 
                            + str(type(self.delta_t))  
                            + "\n Must be a float or int")
        if self.delta_t <= 0:
            raise ValueError("delta_t must be >0")
            
    def check_rate(self):
        """Throw errors if types/values are wrong"""
        if not (isinstance(self.rate, float)
                or isinstance(self.rate, np.ndarray)):
            raise TypeError("Bad operand type for rate: "
                            + str(type(self.rate)) + "\n Must be " 
                            + "float or numpy array of same shape as shape")
        if isinstance(self.rate, float):
            if self.rate > 1 or self.rate < 0:
                raise ValueError("rate is not a probability. " + 
                                 "Must be between 0 and 1 inclusive")
        if isinstance(self.rate, np.ndarray):
            if len(self.rate.shape) == 2:
                if self.rate.shape != self.shape:
                    raise ValueError("mismatched rate shape and shape of images")
                for i in xrange(len(self.rate)):
                    for k in xrange(len(self.rate[i])):
                        if self.rate[i][k] > 1 or self.rate[i][k] < 0:
                            raise ValueError("Some rate values are not " + 
                                             "between 0 and 1 inclusive")
            if len(self.rate.shape) == 3:
                if self.rate.shape != self.shape:
                    raise ValueError("mismatched rate shape and shape of images")
                for i in xrange(len(self.rate)):
                    for k in xrange(len(self.rate[i])):
                        for j in xrange(len(self.rate[i][k])):
                            if (
                                    self.rate[i][k][j] > 1 
                                    or self.rate[i][k][j] < 0):
                                raise ValueError("Some rate values are not " + 
                                                 "between 0 and 1 inclusive")
                if self.n > self.rate.shape[0]:
                    raise ValueError("n is greater than number of individual" + 
                                     "probability arrays in rate")
            else:
                raise ValueError("rate must be 2D or 3D numpy"
                                 +" array (or a float)")
    
    def check_n(self):
        """Throw errors if types/values are wrong"""
        if self.n is not None:
            if not isinstance(self.n, int):
                raise TypeError("Bad operand type for n: "
                                + str(type(self.n)) + "\n Must be int") 
            if self.n < 1:
                raise ValueError("n must be >= 1")
    
    def check_lifetime(self):
        if self.lifetime is None:
            raise ValueError("event lifetime is a required parameter")
        else:
            if not isinstance(self.lifetime, float):
                raise TypeError("lifetime must be int or float")
            if self.lifetime <= 0:
                raise ValueError("event lifetimes must be > 0")
    
    def check_lifetime_sigma(self):
        """Throw errors if types/values are wrong"""
        if self.lifetime_sigma is not None:
            if not isinstance(self.lifetime_sigma, float):
                raise TypeError("Bad operand type for lifetime_sigma: "
                                + str(type(self.lifetime_sigma)) 
                                + "\n Must be float")
            if self.lifetime_sigma <= 0:
                raise ValueError("Sigma of event lifetime is <= 0. Bad!")
    
    def check_gauss_intensity(self):
        """Throw errors if types/values are wrong"""
        if self.gauss_intensity is not None:
            if not isinstance(self.gauss_intensity, float):
                raise TypeError("Bad operand type for gauss_intensity: "
                                + str(type(self.gauss_intensity)) 
                                + "\n Must be float")
            if self.gauss_intensity < 0:
                raise ValueError("Intensity must be >= 0")
    
    def check_gauss_sigma(self):
        """Throw errors if types/values are wrong"""
        if self.gauss_sigma is not None:
            if not isinstance(self.gauss_sigma, float):
                raise TypeError("Bad operand type for gauss_sigma: "
                                + str(type(self.gauss_sigma))
                                + "\n Must be float")
            if self.gauss_sigma <= 0:
                raise ValueError("Sigma of event intensity is <= 0. Bad!")
                                