"""
Class to hold an individual event

"""

import numpy as np
import copy

def zeroFunction(lum=0, loc=0, lifetime=0):
    return 0.0

class TransientEvent:
    """
    """
    def __init__(self, birthLoc, lifetime, classID, 
                 noiseFunction = zeroFunction, noiseExtraArgs = [],
                 luminositySeries = None):
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
            noiseFunction:
                function that adds noise to even luminosity
                Arguments (in this order):
                    lum, loc, lifetime, *noiseExtraArgs
        """
        self.classID = classID
        self.loc = birthLoc
        self.noiseArgs = noiseExtraArgs
        self.history = [copy.copy(birthLoc)]
        self.detectionHistory = []
        self.lifetime = lifetime
        self.noiseFunc = noiseFunction
        if isinstance(luminositySeries, None):
            self.lum = 1 + self.noiseFunc(
                                self.lum, self.loc, self.lifetime,
                                *self.noiseArgs         
                                         )
            self.luminositySeries = [1]
        else:
            self.luminositySeries = luminositySeries
            self.lum = (self.luminositySeries[0]  
                            + self.noiseFunc(
                                        self.lum, 
                                        self.loc, 
                                        self.lifetime,
                                        *self.noiseArgs))
        self.markedForDeath = False
        self.eventID = np.random.randint(2**64, dtype = np.uint64)
        self.holisticDetection = False
        
    
    def advanceEvent(self):
        if not self.markedForDeath:
            self.loc[0] += 1
            self.loc[1] += self.loc[3]
            self.loc[2] += self.loc[4]
            self.history.append(copy.copy(self.loc) + [self.lum])
            self.lum = (self.luminositySeries[
                                self.loc[0] % len(self.luminositySeries)
                                             ])
            self.lum += self.noiseFunc(
                                self.lum, 
                                self.loc, 
                                self.lifetime,
                                *self.noiseArgs)
        
        if self.loc[0] - self.history[0][0] > self.lifetime:
            self.markedForDeath = True
    
    def recordDetection(self, noise):
        """Record a "frame" detection. 
        
        the noise factor is to account for noise in the detector,
        NOT noise in the event itself
        """
        self.detectionHistory.append(copy.copy(self.loc) 
                                     + [self.lum + noise])

