"""
Class to hold an individual event

"""

import numpy as np

class TransientEvent:
    """
    """
    def __init__(self, loc, lifetime, birthtime, luminositySeries = None,  ):
        """
        Arguments:
            loc: iterable of tuples. First position is starting
                location. Second is velocity
            lifetime: float. Number of frames
            birthtime: float. Time of birth
            luminositySeries: Iterable of luminosities as fractions of 
                maximum reportable luminosity. The ith entry in the
                iterable represents the luminosity on the ith frame
                of its existance
        """
        self.loc = loc[0]
        if len(loc) > 1:
                self.velocity = loc[1]
        self.lifetime = lifetime
        self.birthtime = birthtime
        if isinstance(luminositySeries, None):
            self.lum = 1
            self.luminositySeries = [1]
        else:
            self.luminositySeries = luminositySeries
            self.lum = self.luminositySeries[0]
        self.currentTime = 0
        self.markedForDeath = False
    
    def advance(self):
        self.currentTime += 1
        self.lum = self.luminositySeries[self.currentTime]
        self.loc[0] += self.velocity[0]
        self.loc[1] += self.velocity[1]
        if self.currentTime - self.birthtime > self.lifetime:
            self.markedForDeath = True