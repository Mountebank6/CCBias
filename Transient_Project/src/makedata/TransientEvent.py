"""
Class to hold an individual event

"""

import numpy as np
import copy

class TransientEvent:
    """
    """
    def __init__(self, loc, lifetime, luminositySeries = None,  ):
        """
        Arguments:
            loc: length 5 list. Positions:
                0: birth time
                1: birth x-location
                2: birth y-location
                3: x-velocity
                4: y-velocity                
            lifetime: float. Number of frames
            luminositySeries: Iterable of luminosities as fractions of 
                maximum reportable luminosity. The ith entry in the
                iterable represents the luminosity on the ith frame
                of its existance
        """
        self.loc = loc
        self.history = [copy.copy(loc)]
        self.lifetime = lifetime
        if isinstance(luminositySeries, None):
            self.lum = 1
            self.luminositySeries = [1]
        else:
            self.luminositySeries = luminositySeries
            self.lum = self.luminositySeries[0]
        self.markedForDeath = False
    
    def advance(self):
        if not self.markedForDeath:
            self.loc[0] += 1
            self.loc[1] += self.loc[3]
            self.loc[2] += self.loc[4]
            self.history.append(copy.copy(self.loc) + [self.lum])
            self.lum = (self.luminositySeries[
                                self.loc[0] % len(self.luminositySeries)
                                             ])
        
        if self.loc[0] - self.history[0][0] > self.lifetime:
            self.markedForDeath = True