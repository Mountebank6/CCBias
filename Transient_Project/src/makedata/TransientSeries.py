"""
Generate fake sample data for testing.


"""

from __future__ import division
from __builtin__ import str

__author__ = "Theo Faridani"
__version__ = "0.11"

import numpy as np
import astropy.nddata as nd
import copy
from makedata.tools import velmaker

_allowed_types = [np.uint8, np.uint16, np.uint32, np.uint64,
                  np.float16, np.float32, np.float64]

#comment
class TransientSeries:
    """Handle creation and iteration of image set
        
    Args: (see __init__ docstring for more information
        shape
        dt
        n
        rate
        lifetime
        lifetime_sigma
        data_type
        gauss_intensity
        gauss_sigma
    Attributes:
        cur_locations: list of 2-tuples
            lists the locations of the centers of the currently living events
                cur_locations[i], cur_births[i], and 
                cur_durations[i] all refer to the same event
        cur_births: list of floats
            lists the birthtimes of the currently living events
                cur_locations[i], cur_births[i], and 
                cur_durations[i] all refer to the same event
        cur_durations: list of floats
            lists how much time remaining of life the currently living events have
                cur_locations[i], cur_births[i], and 
                cur_durations[i] all refer to the same event   
        t: float
            the current time. Always an integer multuple of dt. 
            (t/dt + 1) images have been generated
            in total for a given t since at t == 0, a starting
            image exists.
        astro_data: astropy.nddata.NDDataRef
            the image data at t. It is an array of intensities in space
    Public Methods:
        new_population():
            set t to 0. set astro_data to the zero array of shape given
            by self.shape. Generate a new random set of events.
        set_intensity_gaussian():
            [SOON TO BE DEPRECATED]
            Look through astro_data and cur_locations. If 
            cur_locations indicates an event exists at an index, but 
            the intensity at that index is 0, give that pixel in astro_data
            a gaussian intensity with mean and standard deviation given by
            gauss_intensity and gauss_sigma respectively.
    """
    
    
    def __init__(self, shape=None, dt=None,
                 n=None, rate=None, lifetime=None, 
                 lifetime_sigma=None, data_type=np.uint16,
                 gauss_intensity=None, gauss_sigma=None):
        """Generate initial conditions from parameters.
        
        Args:
            shape: tuple of ints. Required
                Shape of the images in the series. Units of pixels.
            dt: float. Required
                Time elapsed between images
            n: int
                Total number of images to make. (e.g. n*dt = Total observing
                time)
            rate: float or array of floats. Required
                for rate as a float: the probability per pixel per dt
                    that an event spawns
                for rate as an array of floats:
                    the shape of this array must be the same shape as the shape
                    variable given earlier. The entries in this array are
                    the probabilities per dt that an event spawns
                    at the same index in the image. e.g. if rate[40,500] == 0.01,
                    there is a 1% chance per dt that an event will spawn
                    at index [40,500] in the image array.
            lifetime: float. Required
                the average lifetime of the events
            lifetime_sigma: float
                the standard deviation of lifetime. lifetimes generated will
                be from a normal distribution
            data_type: numpy data type
                the data type of the intensity entries in the image.
                Must be one of [np.uint8, np.uint16, np.uint32, np.uint64,
                np.float16, np.float32, np.float64]
            gauss_intensity: float
                Average intensity of the events
            gauss_sigma: float
                standard deviation of the intensities of the events       
        """
        
        self.shape = shape
        self.n = n
        self.dt = dt
        self.rate = rate
        self.data_type = data_type
        self.lifetime = float(lifetime)
        self.lifetime_sigma = float(lifetime_sigma)
        self.gauss_intensity = float(gauss_intensity)
        self.gauss_sigma = float(gauss_sigma)
        self.astro_data = nd.NDDataRef(np.zeros(self.shape, self.data_type))
        
        if self.shape is None:
            raise TypeError("Required argument 'shape' (pos 1) not found")
        if self.dt is None:
            raise TypeError("Required argument 'dt' (pos 2) not found")
        
        self.check_shape()
        self.check_data_type()
        self.check_dt()
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
    
    def populate(self, initial=None):
        """Make some new events
        
        Iterate through the image array, if rate is a float, generate a 
        random number uniformly from 0 to 1. If it's less than rate, put 
        a new event at the location in the image array given by the place
        in the loop. 
        If rate is an array with shape given by a tuple of length 2,
        each pixel of the image array is given a corresponding probability 
        of event generation from the same location in the rate array.
        The events are given lifetimes according to a normal distribution,
        and are given a birth time pulled uniformly from the
        time interval [-dt,0]
        If the rate is an array with shape given by a tuple of length 3, the
        code interprets this as you supplying a (self.n,self.shape[0],
        self.shape[1]) shaped array. In other words, each step in time gets its own
        probability heatmap. (e.g. rate[3] gives the probability heatmap after
        3 dt's of time have passed.
        """
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
                        if initial is True:
                            birth = np.random.uniform(self.t - lifetime, self.t)
                        else:
                            birth = np.random.uniform(self.t - self.dt, self.t)
                        self.cur_births.append(birth)
                        self.cur_locations.append((i,k))
                        self.cur_durations.append(lifetime - (self.t-birth))
                        
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
                            if initial is True:
                                birth = np.random.uniform(self.t - lifetime, self.t)
                            else:
                                birth = np.random.uniform(self.t - self.dt, self.t)
                            self.cur_births.append(birth)
                            self.cur_locations.append((i,k))
                            self.cur_durations.append(lifetime - (self.t-birth))
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
                            if initial is True:
                                birth = np.random.uniform(self.t - lifetime, self.t)
                            else:
                                birth = np.random.uniform(self.t - self.dt, self.t)
                            self.cur_births.append(birth)
                            self.cur_locations.append((i,k))
                            self.cur_durations.append(lifetime - (self.t-birth))
        #kill events that run out of life before t == 0.
        for i in range(len(self.cur_durations)):
            if self.cur_durations[i] <= 0:
                del self.cur_durations[i]
                del self.cur_births[i]
                del self.cur_durations[i]
    
    def new_population(self):
        """Generate fresh transient population and clear old one"""
        self.t = 0.0
        self.cur_locations = []
        self.cur_births = []
        self.cur_durations = []
        self.populate(initial=True)
    
    def advance(self, filename=None):
        if filename is not None:
            if isinstance(filename, str):
                self.astro_data.write(filename)
            else:
                raise TypeError("Bad filename type")
        #TODO: add velocity ticking
        
        #advance time and clean dead events
        self.t += self.dt
        for i in range(len(self.cur_durations)):
            self.cur_durations[i] -= self.dt
            if self.cur_durations[i] <= 0:
                del self.cur_durations[i]
                del self.cur_births[i]
                del self.cur_durations[i]
                
        #generate new events
        self.populate()
        #kill events that live their entire lifetime in between snapshots
        for i in range(len(self.cur_durations)):
            if self.cur_durations[i] <= 0:
                del self.cur_durations[i]
                del self.cur_births[i]
                del self.cur_durations[i]
        return
    
    def set_intensity_guassian(self,mag,sigma):
        """Give new events gaussian intensity"""
        for index in self.cur_locations:
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
                
    def check_dt(self):
        """Throw errors if types/values are wrong"""
        if not (isinstance(self.dt, float) 
                or isinstance(self.dt, int)):
            raise TypeError("Bad operand type for dt: " 
                            + str(type(self.dt))  
                            + "\n Must be a float or int")
        if self.dt <= 0:
            raise ValueError("dt must be >0")
            
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
                                
    def get_shape(self):
        return self.shape
    
    def get_n(self):
        return self.n
    
    def get_dt(self):
        return self.dt
    
    def get_rate(self):
        return self.rate
    
    def get_data_type(self):
        return self.data_type
    
    def get_lifetime(self):
        return self.lifetime
    
    def get_lifetime_sigma(self):
        return self.lifetime_sigma
    
    def get_gauss_intensity(self):
        return self.gauss_intensity
    
    def get_gauss_sigma(self):
        return self.gauss_sigma
    
    def get_astro_data(self):
        return self.astro_data
    
    def get_current_time(self):
        return self.t
    
    def get_cur_locations(self):
        return self.cur_locations
    
    def get_cur_births(self):
        return self.cur_births
    
    def get_cur_durations(self):
        return self.cur_durations
    
    def set_shape(self, new):
        temp = copy.copy(self.shape)
        self.shape = new
        try:
            self.check_shape()
        except:
            self.shape = temp
            raise ValueError("new not compliant with documentation")
        
    def set_dt(self, new):
        temp = copy.copy(self.dt)
        self.dt = new
        try:
            self.check_dt()
        except:
            self.dt = temp
            raise ValueError("not compliant with documentation")
    
    def set_n(self, new):
        temp = copy.copy(self.n)
        self.n = new
        try:
            self.check_n()
        except:
            self.n = temp
            raise ValueError("new not compliant with documentation")
    
    def set_rate(self, new):
        temp = copy.copy(self.rate)
        self.rate = new
        try:
            self.check_rate()
        except:
            self.rate = temp
            raise ValueError("new not compliant with documentation")
    
    def set_data_type(self, new):
        temp = copy.copy(self.data_type)
        self.data_type = new
        try:
            self.check_data_type()
        except:
            self.data_type = temp
            raise ValueError("new not compliant with documentation."
                            +" You also probably shouldn't be changing this")
    
    def set_lifetime(self, new):
        temp = copy.copy(self.lifetime)
        self.lifetime = new
        try:
            self.check_lifetime()
        except:
            self.lifetime = temp
            raise ValueError("new not compliant with documentation")
        
    def set_lifetime_sigma(self, new):
        temp = copy.copy(self.lifetime_sigma)
        self.lifetime_sigma = new
        try:
            self.check_lifetime_sigma()
        except:
            self.lifetime_sigma = temp
            raise ValueError("new not compliant with documentation")
        
    def set_gauss_intensity(self, new):
        temp = copy.copy(self.gauss_intensity)
        self.gauss_intensity = new
        try:
            self.check_gauss_intensity()
        except:
            self.gauss_intensity = temp
            raise ValueError("new not compliant with documentation")
        
    def set_gauss_sigma(self, new):
        temp = copy.copy(self.gauss_sigma)
        self.gauss_sigma = new
        try:
            self.check_gauss_sigma()()
        except:
            self.gauss_sigma = temp
            raise ValueError("new not compliant with documentation")
    