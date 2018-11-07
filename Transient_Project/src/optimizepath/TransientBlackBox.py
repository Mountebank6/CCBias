"""
A class that turns the survey object into a blackbox function.

This assumes that all characteristic ranges are in float.
Integer support will be deprecated
"""

import numpy as np
from . import fixedPlackettBurman as doe
from scipy import linalg

class TransientBlackBox:
    """
    as
    """
    def __init__(self, survey, runTime, lossFunction, comparisonData):
        """
        Args:
            survey:
                The initialized survey object to optimize over
            surveyTime:
                The number of frames to run the survey each generation
            lossFunction:
                Function. Returns the deviation from comparisonData
                    Always returns values >= 0
                    Args: 
                        survey:
                            The survey to be scored
                        comparisonData:
                            The data to score against

        """

        self.surv = survey
        self.runTime = runTime
        self.loss = lossFunction
        self.comparisonData = comparisonData
        self.rawChar = self.unpackRawCharacteristicPositionVector(self.surv)

    def returnValue(self, scaledVec):
        """Return the BlackBox function value at the given scaled position
        
        Args:
            scaledVec:
                """
        value = 0
        return value
    #Global Raw and Scaling
    def scaledVecToRawVec(self, scaledVec):
        """Return the raw form of input scaledVec"""
        rawVec = []
        for i in range(len(scaledVec)):
            raw = (scaledVec*((self.rawChar[i][1]-self.rawChar[i][0])/2)
                  +((self.rawChar[i][1]+self.rawChar[i][0])/2))
            rawVec.append(raw)
        return rawVec

    def rawVecToScaledVec(self, rawVec):
        """Return the scaled form of input rawVec"""
        scaledVec = []
        for i in range(len(rawVec)):
            delta = rawVec[i] - ((self.rawChar[i][1]+self.rawChar[i][0])/2)
            scaled = delta/((self.rawChar[i][1]-self.rawChar[i][0])/2)
            scaledVec.append(scaled)
        return scaledVec

    #Local Scaling to Global Scaling and vice versa
    def globalScaledToLocalScaled(self, globalScaled, radius):
        return
    
    #For prescreening
    def localPlackettBurmann(self, scaledVec, trustRadius):
        """Return the weights of a local PlackettBurman experiment
        
        scaledVec and trustRadius are in global scaled 'units'
        """
        dim = len(scaledVec)
        success = False
        i = 0
        #We need to do this wacky method because doe procs an error
        #when n is certain values. This results in 10-30% longer matrices for
        #n > 30. Unsure the exact distribution. 
        #Probably has to do with prime number density or something
         
        while success is False:
            try:
                experimentMatrix = doe.pbdesign(dim + 4*i)
                success = True
                i += 1
            except:
                i += 1
        experimentMatrix = experimentMatrix[:,:dim]
        
        #experimentMatrix is D, now we construct X
        unitLength = trustRadius/np.sqrt(dim)
        experimentMatrix *= unitLength
        for i in range(len(experimentMatrix)):
            experimentMatrix[i] += scaledVec.T
            for k in range(len(experimentMatrix[i][k])):
                if experimentMatrix[i][k] > 1:
                    experimentMatrix[i][k] = 1
                elif experimentMatrix[i][k] < -1:
                    experimentMatrix[i][k] = -1
        resultsVec = np.zeros((len(experimentMatrix),1))
        for i in range(len(resultsVec)):
            resultsVec[i] = self.returnValue(experimentMatrix[i].T)

        #Now we solve for beta, the least-squares estimator
        A = experimentMatrix.T.dot(experimentMatrix)
        beta = np.linalg.solve(A, experimentMatrix.dot(resultsVec))
        return beta

    def localResolutionIII(self, scaledVec, trustRadius, 
                           importantIndeces, repetition):
        """Return a function that models the space to first order"""
        meanValue = 0
        for _ in range(repetition):
            meanValue += self.returnValue(scaledVec)
        meanValue /= repetition

        
        return

    def unpackRawCharacteristicPositionVector(self, survey):
        """Return a flattened characteristic vector
        
        First come the generator values, then the observing profile values
        """
        charPositionVec = []
        charGenBias = survey.generator.charBias

        charObsBias = (survey.profile.vCharBias
                      +survey.profile.oCharBias
                      +survey.profile.hCharBias
                      +survey.profile.sCharBias)
        
        for i in range(len(charGenBias)):
            for k in range(len(charGenBias[i])):
                charPositionVec += charGenBias[i][k]
        charPositionVec += charObsBias
        
        return charPositionVec

    