"""
Generate fake sample data for testing.


"""


__author__ = "Theo Faridani"
__version__ = "0.11"

import numpy as np
import astropy.nddata as nd
import copy
from .tools import velmaker
import math

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
        cur_locs: list of 2-tuples
            lists the locations of the centers of the currently living events
                cur_locs[i], cur_births[i], and 
                cur_durations[i] all refer to the same event
        cur_births: list of floats
            lists the birthtimes of the currently living events
                cur_locs[i], cur_births[i], and 
                cur_durations[i] all refer to the same event
        cur_durations: list of floats
            lists how much time remaining of life the currently living events have
                cur_locs[i], cur_births[i], and 
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
            ["SOON" TO BE DEPRECATED]
            Look through astro_data and cur_locs. If 
            cur_locs indicates an event exists at an index, but 
            the intensity at that index is 0, give that pixel in astro_data
            a gaussian intensity with mean and standard deviation given by
            gauss_intensity and gauss_sigma respectively.
    """
    
    
    def __init__(self, shape=None, dt=None,
                 n=None, rate=None, lifetime=None, 
                 lifetime_sigma=None, data_type=np.uint16,
                 gauss_intensity=None, gauss_sigma=None, unifv=None,
                 filename=None):
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
            unifv: float
                velocity that all events have in 3D space
                then this is projected onto the plane
            filename: str
                the standard name of the images. the time and extension
                are automatically placed after it. (e.g. filename="dave")
                results in files like dave0.0.fits, dave1.0.fits, etc)
        """
        
        self.shape = shape
        self.n = n
        self.dt = dt
        self.rate = rate
        self.data_type = data_type
        self.lifetime = float(lifetime)
        self.lifetime_sigma = lifetime_sigma
        self.gauss_intensity = gauss_intensity
        self.gauss_sigma = gauss_sigma
        self.unifv = unifv
        self.filename = filename
        self.valid_i = range(shape[0])
        self.valid_j = range(shape[1])
        self.astro_data = nd.CCDData(
                                     np.zeros(self.shape, self.data_type),
                                     unit="adu")
        
        if self.shape is None:
            raise TypeError("Required argument 'shape' (pos 1) not found")
        if self.dt is None:
            raise TypeError("Required argument 'dt' (pos 2) not found")
        
        self.__check_shape()
        self.__check_data_type()
        self.__check_dt()
        self.__check_rate()
        self.__check_n()
        self.__check_lifetime()
        self.__check_lifetime_sigma()
        self.__check_gauss_intensity()
        self.__check_gauss_sigma()
        self.__check_unifv()
        self.__check_filename()

        self.new_population()
        if self.gauss_intensity is not None:
            if self.gauss_sigma is not None:
                self.set_intensity_gaussian(gauss_intensity, gauss_sigma)
            else:
                self.set_intensity_gaussian(gauss_intensity, 0.000001)
    
    def populate(self):
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
            self.__float_rate_populate()
                        
        if isinstance(self.rate, np.ndarray):
            if len(self.rate.shape) == 2:
                self.__array2_rate_populate()
            else:
                self.__array3_rate_populate()
        #kill events that run out of life before t == 0.
        self.__kill_dead_events(tick_time=False)
        
        if self.gauss_intensity is not None and self.gauss_sigma is not None:
            self.__update_image_gaussian()
        else:
            self.__update_image_pointwise()
    
    def new_population(self):
        """Generate fresh transient population and clear old one"""
        #locs is the integer values locations
        #raw_locs is the float valued locations
        self.t = 0.0
        self.cur_locs = []
        self.cur_raw_locs = []
        self.cur_births = []
        self.cur_durations = []
        self.cur_vels = []
        self.cur_intens = []
        self.__pre_populate()
    
    def __pre_populate(self):
        """Go back in time to generate sensible initial images"""
        iters = math.ceil(2*self.lifetime/self.dt)
        self.t -= iters*self.dt
        for _ in range(iters):
            self.advance(filename=None)
    
    def advance(self, filename=1):
        """Increment the data by one dt
        
        Set filename to None in order to not write
        """
        if filename is not None:
            filename = self.filename
            self.astro_data.write(filename + str(self.t) + ".fits")
        
        #advance time and clean dead events
        self.t += self.dt
        self.__kill_dead_events(tick_time=True)
        
        #tick event velocities
        for i in range(len(self.cur_vels)):
            self.cur_raw_locs[i][0] += self.dt*self.cur_vels[i][0]
            self.cur_raw_locs[i][1] += self.dt*self.cur_vels[i][1]
            self.cur_locs[i][0] = int(round(self.cur_raw_locs[i][0]))
            self.cur_locs[i][1] = int(round(self.cur_raw_locs[i][1]))
          
        #generate new events
        self.populate()
        #kill events that live their entire lifetime in between snapshots
        self.__kill_dead_events(tick_time=False)
        return
    
    def advance_to_end(self):
        """Generate the whole suite of images"""
        if self.n is None:
            raise ValueError("n must be given")
        while self.t < self.dt*self.n:
            self.advance(self.filename)
    
    def set_intensity_gaussian(self,mag,sigma):
        """Give new events gaussian intensity
        
        REALLY STUPID!!!! DON'T USE THIS!!!!
        """
        for index in self.cur_locs:
            if self.astro_data.data[index] == 0:
                self.astro_data.data[index] = np.random.normal(mag,sigma)
                
    def __assign_intensity(self):
        if self.gauss_intensity is not None:
            if self.gauss_sigma is None:
                return np.random.normal(self.gauss_intensity, 0.000001)
            else:
                return np.random.normal(self.gauss_intensity, self.gauss_sigma)
        else:
            try:
                max_value = np.iinfo(self.data_type).max
            except:
                pass
            try:
                max_value = np.finfo(self.data_type).max
            except:
                pass
            return max_value
    
    def __append_event(self, birth, loc, duration, vel, inten):
        self.cur_births.append(birth)
        self.cur_locs.append(loc)
        self.cur_raw_locs.append(loc)
        self.cur_durations.append(duration)
        self.cur_vels.append(vel)
        self.cur_intens.append(inten)
    
    def __kill_dead_events(self, tick_time=False):
        badindex = []
        for i in range(len(self.cur_durations)):
            if tick_time is True:
                self.cur_durations[i] -= self.dt
            if self.cur_durations[i] <= 0:
                badindex.insert(0, i)
        for index in badindex:
            del self.cur_durations[index]
            del self.cur_births[index]
            del self.cur_locs[index]
            del self.cur_raw_locs[index]
            del self.cur_vels[index]
            del self.cur_intens[index]
    
    def __update_image(self):
        self.astro_data.data = np.zeros(self.shape, dtype=self.data_type)
        for i in range(len(self.cur_locs)):
            if self.cur_locs[i][0] in self.valid_i:
                if self.cur_locs[i][1] in self.valid_j:
                    self.astro_data.data[tuple(self.cur_locs[i])] = (
                                                            self.cur_intens[i])
    
    def __update_image_pointwise(self):
        self.astro_data.data = np.zeros(self.shape, dtype=self.data_type)
        try:
            max_value = np.iinfo(self.data_type).max
        except:
            pass
        try:
            max_value = np.finfo(self.data_type).max
        except:
            pass
        for loc in self.cur_locs:
            if loc[0] in self.valid_i:
                if loc[1] in self.valid_j:
                    self.astro_data.data[tuple(loc)] = max_value
    
    def __update_image_gaussian(self):
        self.astro_data.data = np.zeros(self.shape, dtype=self.data_type)
        for loc in self.cur_locs:
            if loc[0] in self.valid_i and loc[1] in self.valid_j:
                self.astro_data.data[tuple(loc)] = np.random.normal(
                                                            self.gauss_intensity,
                                                            self.gauss_sigma)
    
    def __float_rate_populate(self):
        for i in range(len(self.astro_data.data)):
            for k in range(len(self.astro_data.data[i])):   
                if np.random.rand() < self.rate:
                    if self.lifetime_sigma is not None:
                        lifetime = np.random.normal(
                                            self.lifetime,
                                            self.lifetime_sigma)
                    else:
                        lifetime = self.lifetime
                    birth = np.random.uniform(self.t - self.dt, self.t)
                    self.__append_event(
                                        birth, [i,k], lifetime - (self.t-birth), 
                                        self.unifv*velmaker.get_unifv(), 
                                        self.__assign_intensity())
    
    def __array2_rate_populate(self):
        for i in range(len(self.astro_data.data)):
            for k in range(len(self.astro_data.data)):
                if np.random.rand() < self.rate[i][k]:
                    if self.lifetime_sigma is not None:
                        lifetime = np.random.normal(
                                            self.lifetime,
                                            self.lifetime_sigma)
                    else:
                        lifetime = self.lifetime
                    birth = np.random.uniform(self.t - self.dt, self.t)
                    self.__append_event(
                                        birth, [i,k], lifetime - (self.t-birth), 
                                        self.unifv*velmaker.get_unifv(), 
                                        self.__assign_intensity())
                            
    def __array3_rate_populate(self):
        for i in range(len(self.astro_data.data)):
            for k in range(len(self.astro_data.data)):
                if np.random.rand() < self.rate[int(round(self.t/self.dt))][i][k]:
                    if self.lifetime_sigma is not None:
                        lifetime = np.random.normal(
                                            self.lifetime,
                                            self.lifetime_sigma)
                    else:
                        lifetime = self.lifetime
                    birth = np.random.uniform(self.t - self.dt, self.t)
                    self.__append_event(
                                        birth, [i,k], lifetime - (self.t-birth), 
                                        self.unifv*velmaker.get_unifv(), 
                                        self.__assign_intensity())
    
    def __check_shape(self):
        """Throw errors if types/values are wrong"""
        if not isinstance(self.shape, tuple):
            raise TypeError("Bad operand type for shape: " 
                            + str(type(self.shape)))
        if len(self.shape) != 2:
            raise ValueError("shape is not of length 2")
        for x in self.shape:
            if not isinstance(x, int):
                raise TypeError("shape tuple must contain ints")
        
    def __check_data_type(self):
        """Throw errors if types/values are wrong"""
        if self.data_type not in _allowed_types:
            raise TypeError("Bad operand type for data_type: " 
                            + str(type(self.data_type)) + "\n Must be"
                            + "one of " + str(_allowed_types))
                
    def __check_dt(self):
        """Throw errors if types/values are wrong"""
        if not (isinstance(self.dt, float) 
                or isinstance(self.dt, int)):
            raise TypeError("Bad operand type for dt: " 
                            + str(type(self.dt))  
                            + "\n Must be a float or int")
        if self.dt <= 0:
            raise ValueError("dt must be >0")
            
    def __check_rate(self):
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
                for i in range(len(self.rate)):
                    for k in range(len(self.rate[i])):
                        if self.rate[i][k] > 1 or self.rate[i][k] < 0:
                            raise ValueError("Some rate values are not " + 
                                             "between 0 and 1 inclusive")
            if len(self.rate.shape) == 3:
                if self.rate.shape != self.shape:
                    raise ValueError("mismatched rate shape and shape of images")
                for i in range(len(self.rate)):
                    for k in range(len(self.rate[i])):
                        for j in range(len(self.rate[i][k])):
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
    
    def __check_n(self):
        """Throw errors if types/values are wrong"""
        if self.n is not None:
            if not isinstance(self.n, int):
                raise TypeError("Bad operand type for n: "
                                + str(type(self.n)) + "\n Must be int") 
            if self.n < 1:
                raise ValueError("n must be >= 1")
    
    def __check_lifetime(self):
        if self.lifetime is None:
            raise ValueError("event lifetime is a required parameter")
        else:
            if not isinstance(self.lifetime, float):
                raise TypeError("lifetime must be int or float")
            if self.lifetime <= 0:
                raise ValueError("event lifetimes must be > 0")
    
    def __check_lifetime_sigma(self):
        """Throw errors if types/values are wrong"""
        if self.lifetime_sigma is not None:
            if not isinstance(self.lifetime_sigma, float):
                try: 
                    self.lifetime_sigma = float(self.lifetime_sigma)
                except:
                    raise TypeError("Bad operand type for lifetime_sigma: "
                                    + str(type(self.lifetime_sigma)) 
                                    + "\n Must be float")
            if self.lifetime_sigma <= 0:
                raise ValueError("Sigma of event lifetime is <= 0. Bad!")
    
    def __check_gauss_intensity(self):
        """Throw errors if types/values are wrong"""
        if self.gauss_intensity is not None:
            if not isinstance(self.gauss_intensity, float):
                try:
                    self.gauss_intensity = float(self.gauss_intensity)
                except:
                    raise TypeError("Bad operand type for gauss_intensity: "
                                    + str(type(self.gauss_intensity)) 
                                    + "\n Must be float")
            if self.gauss_intensity < 0:
                raise ValueError("Intensity must be >= 0")
    
    def __check_gauss_sigma(self):
        """Throw errors if types/values are wrong"""
        if self.gauss_sigma is not None:
            if not isinstance(self.gauss_sigma, float):
                try:
                    self.gauss_sigma = float(self.gauss_sigma)
                except:
                    raise TypeError("Bad operand type for gauss_sigma: "
                                    + str(type(self.gauss_sigma))
                                    + "\n Must be float")
            if self.gauss_sigma <= 0:
                raise ValueError("Sigma of event intensity is <= 0. Bad!")
    
    def __check_unifv(self):
        if self.unifv is not None:
            if not isinstance(self.unifv, float):
                try:
                    self.unifv = float(self.unifv)
                except:
                    raise TypeError("Bad operand type for gauss_intensity: "
                                    + str(type(self.unifv)) 
                                    + "\n Must be float")
            if self.unifv < 0:
                raise ValueError("unifv must be positive")
    
    def __check_filename(self):
        if self.filename is not None:
            if not isinstance(self.filename, str):
                raise TypeError("Bad operand type for gauss_intensity: "
                                    + str(type(self.filename)) 
                                    + "\n Must be string")
                                
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
        return self.cur_locs
    
    def get_cur_births(self):
        return self.cur_births
    
    def get_cur_durations(self):
        return self.cur_durations
    
    def set_shape(self, new):
        temp = copy.copy(self.shape)
        self.shape = new
        try:
            self.__check_shape()
        except:
            self.shape = temp
            raise ValueError("new not compliant with documentation")
        
    def set_dt(self, new):
        temp = copy.copy(self.dt)
        self.dt = new
        try:
            self.__check_dt()
        except:
            self.dt = temp
            raise ValueError("not compliant with documentation")
    
    def set_n(self, new):
        temp = copy.copy(self.n)
        self.n = new
        try:
            self.__check_n()
        except:
            self.n = temp
            raise ValueError("new not compliant with documentation")
    
    def set_rate(self, new):
        temp = copy.copy(self.rate)
        self.rate = new
        try:
            self.__check_rate()
        except:
            self.rate = temp
            raise ValueError("new not compliant with documentation")
    
    def set_data_type(self, new):
        temp = copy.copy(self.data_type)
        self.data_type = new
        try:
            self.__check_data_type()
        except:
            self.data_type = temp
            raise ValueError("new not compliant with documentation."
                            +" You also probably shouldn't be changing this")
    
    def set_lifetime(self, new):
        temp = copy.copy(self.lifetime)
        self.lifetime = new
        try:
            self.__check_lifetime()
        except:
            self.lifetime = temp
            raise ValueError("new not compliant with documentation")
        
    def set_lifetime_sigma(self, new):
        temp = copy.copy(self.lifetime_sigma)
        self.lifetime_sigma = new
        try:
            self.__check_lifetime_sigma()
        except:
            self.lifetime_sigma = temp
            raise ValueError("new not compliant with documentation")
        
    def set_gauss_intensity(self, new):
        temp = copy.copy(self.gauss_intensity)
        self.gauss_intensity = new
        try:
            self.__check_gauss_intensity()
        except:
            self.gauss_intensity = temp
            raise ValueError("new not compliant with documentation")
        
    def set_gauss_sigma(self, new):
        temp = copy.copy(self.gauss_sigma)
        self.gauss_sigma = new
        try:
            self.__check_gauss_sigma()
        except:
            self.gauss_sigma = temp
            raise ValueError("new not compliant with documentation")
    