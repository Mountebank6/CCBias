"""
Generate fake sample data for testing.
Deprecated because I'm just going to use other people's code to handle this


"""

__author__ = "Theo Faridani"
__version__ = "0.1"

import numpy as np

class ImageData:
    """Create and store a single frame of image data."""
    
    def __init__(self, xdim=0, ydim=0):
        """Create array of zeros with a given shape.
        
        Keyword arguments:
        xdim -- the width of the image array (default 0)
        ydim -- the height of the image array (default 0)
        """
        
        self.x = xdim
        self.y = ydim
        self.data = np.zeros((self.y,self.x),dtype=np.uint16)
    
    def fill(self, newdata=None):
        """Change self.data to a new, given array of the same shape.
        
        Keyword arguments:
        newdata -- the new numpy ndarray of image data. Must have same
                   shape as self.data.
        
        If no newdata is given (i.e. x.fill() is called), then it sets
        self.data to an array of zeros of the appropriate shape)
        """
        if newdata is None:
            newdata = np.zeros((self.y,self.x),dtype=np.uint16)
        if isinstance(newdata, np.ndarray) == False:
            raise TypeError("newdata is not of type numpy.ndarray")
        if newdata.shape != self.data.shape:
            raise IndexError("shape of new data is different than " + 
                             "shape of old data")
        if newdata.dtype != np.uint16:
            raise TypeError("Newdata has wrong datatype in its " +
                            "entries. Has " + str(newdata.dtype) +
                            " Needs uint16.")
        self.data = newdata
        
    def change(self, deltas=None):
        """Change self by giving a list of what should be changed.
        
        Keyword arguments:
        deltas -- A list of ordered pairs associated with new values.
        Each entry in the deltas list has the following format:
        [tuple, value] where the tuple is (ylocation,xlocation) for
        the value to be placed.
        """
        if deltas is None:
            deltas = []
        for i in xrange(len(deltas)):
            self.data[deltas[i][0]] = deltas[i][1]
            
    def replacedata(self, newdata=None):
        """Replace self.data with new data of different shape  
        
        This funcionality is kept intentionally separate from 
        ImageData.fill to prevent accidental changing of array shape.
        
        Keyword arguments:
        newdata -- the new numpy ndarray of image data. Can
                   have different shape than current data.
        """
        if isinstance(newdata, np.ndarray) == False:
            raise TypeError("newdata is not of type numpy.ndarray")
        if newdata.dtype != np.uint16:
            raise TypeError("Newdata has wrong datatype in its " +
                            "entries. Has " + str(newdata.dtype) +
                            " Needs uint16.")
        self.y = newdata.shape[0]
        self.x = newdata.shape[1]
        self.data = newdata