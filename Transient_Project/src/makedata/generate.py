"""
Generate fake sample data for testing.


"""

__author__ = "Theo Faridani"
__version__ = "0.1"

import numpy as np

class ImageData:
    """Create and store a single frame of image data."""
    
    def __init__(self, xdim=0, ydim=0):
        """Create array of zeros with a given shape.
        
        Only rectangular data allowed.
        """
        
        self.x = xdim
        self.y = ydim
        self.data = np.zeros((self.x,self.y),dtype=np.uint8)
    
    def fill(self, newdata=None):
        """Change self.data to a new, given array of the same size."""
        if newdata == None:
            newdata = np.zeros((self.x,self.y),dtype=np.uint8)
        if newdata.dtype != np.dtype('uint8'):
            raise TypeError('Newdata has wrong datatype. Needs uint8.')
        if newdata.size != self.data.size:
            raise IndexError('Size of new data is different than ' + 
                             'size of old data')
        self.data = newdata
        
    def change(self, deltas=None):
        """Change self by giving a list of what should be changed.
        
        The deltas argument must be formatted as a list where each
        entry is another list of length 3. In these length 3 lists,
        indexes 0 and 1 describe what index in self.data should be 
        changed, and index 2 gives the value it should be changed to.
        """
        if deltas == None:
            deltas = []
        for i in xrange(len(deltas)):
            self.data[deltas[i][0],deltas[i][1]] = deltas[i][2]
            