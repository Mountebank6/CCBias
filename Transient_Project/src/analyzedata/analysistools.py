"""Useful tools for looking at image data

"""
import numpy as np
import copy

#There's 5 cases when you look at a place
#no event is there
#you're looking at an event but it's not emitting: duty cycle is 
#   currently off
#it's there and emitting but obscured by something
#it's there and emitting and unobscured but too noisy to detect
#it's there and emitting and you see it

def addGaussianNoise(inputArray, noiseMean, noiseSigma):
    """Adds normally distributed noise to all elements"""
    if not isinstance(inputArray, np.ndarray):
        final = np.asarray(copy.deepcopy(inputArray))
    else:
        final = copy.deepcopy(inputArray)
    final += np.random.normal(noiseMean, noiseSigma, final.size)

def calcSNR(inputArray, loc):
    """Calc SNR of the loc
    
    The noise is defined to be the standard deviation
    of all points in the array. Here, we strip data
    with value > 3 sigma, then use the std dev of the
    remainig data to set our value for the noise
    """
    dfc = copy.deepcopy(inputArray.flatten())
    std = np.std(inputArray)
    rude = np.mean(inputArray)
    for i in (range(len(dfc))[::-1]):
        if np.abs(dfc[i]) > (3*std + np.abs(rude)):
            del dfc[i]
    fixedStd = np.std(dfc)
    return inputArray[loc]/fixedStd


