"""
A class that turns the survey object into a blackbox function.
The output is the distance between the comparisonData and the
    generated data.

This assumes that all characteristic ranges are in float.
Integer support will be deprecated
"""

import numpy as np

class TransientBlackBox:
    """
    as
    """
    def __init__(self, survey, runTime, lossFunction, comparisonData):
        """
        Args:
            survey:
                The initialized survey object to optimize over
            runTime:
                The number of frames to run the survey each generation
            lossFunction:
                Function. Returns the deviation from comparisonData
                    Always returns values >= 0, goal is to minimize this value

                    Args: 
                        survey:
                            The survey to be scored
                        comparisonData:
                            The data to score against
            comparisonData:
                The "observed in real-life data" to mimic

        """

        self.surv = survey
        self.runTime = runTime
        self.loss = lossFunction
        self.comparisonData = comparisonData
        self.rawChar = self.unpackRawCharacteristicPositionVector()

    def returnValue(self, scaledVec):
        """Return the BlackBox function value at the given scaled position
        
        Args:
            scaledVec:
                position vector in the [-1,1]^N nondimensional parameter space
        """
        self.applyNewParams(scaledVec)
        self.surv.reRunSurvey(self.runTime)
        return self.loss(self.surv, self.comparisonData)

    def scaledVecToRawVec(self, scaledVec):
        """Return the raw form of input scaledVec"""
        rawVec = []
        for i in range(len(scaledVec)):
            raw = (scaledVec[i]*((self.rawChar[i][1]-self.rawChar[i][0])/2)
                  +((self.rawChar[i][1]+self.rawChar[i][0])/2))
            rawVec.append(raw)
        return rawVec

    def rawVecToScaledVec(self, rawVec):
        """Return the scaled form of input rawVec"""
        scaledVec = []
        for i in range(len(rawVec)):
            if self.rawChar[i][1] == self.rawChar[i][0]:
                scaledVec.append(0)
            else:
                delta = rawVec[i] - ((self.rawChar[i][1]+self.rawChar[i][0])/2)
                scaled = delta/((self.rawChar[i][1]-self.rawChar[i][0])/2)
                scaledVec.append(scaled)
        return scaledVec

    def applyNewParams(self, scaledVec):
        rawVec = self.scaledVecToRawVec(scaledVec)
        surv = self.surv
        genExtraArgs = []
        l = self.surv.generator.eArgs
        numGenArgs = len([item for sublist in l for item in sublist])
        
        for _ in range(len(self.surv.generator.eArgs)):
            genExtraArgs.append([])
        vArgs = []
        lenV = len(self.surv.profile.vCharBias)
        oArgs = []
        lenO = len(self.surv.profile.oCharBias)
        hArgs = []
        lenH = len(self.surv.profile.hCharBias)
        sArgs = []
        lenS = len(self.surv.profile.sCharBias)
        assert len(rawVec) == lenV + lenO + lenH + lenS + numGenArgs

        for i in range(len(rawVec)):
            if i in range(lenV):
                vArgs.append(rawVec[i])
            elif i - lenV in range(lenO):
                oArgs.append(rawVec[i])
            elif i - lenV - lenO in range(lenH):
                hArgs.append(rawVec[i])
            elif i - lenV - lenO - lenH in range(lenS):
                sArgs.append(rawVec[i]) 
            else:
                genStart = i
                break
        for i in range(len(rawVec)-genStart):
            offset = 0
            for j in range(len(genExtraArgs)):
                if i < len(self.surv.generator.eArgs[j]) + offset:
                    k = j
                    break
                else:
                    offset += len(self.surv.generator.eArgs[j])
            genExtraArgs[k].append(rawVec[i+genStart])
        
        surv.setObservingProfileArgs(vArgs, oArgs, hArgs, sArgs)
        surv.setGeneratorFunctionArgs(genExtraArgs)

    def unpackRawCharacteristicPositionVector(self):
        """Return a flattened characteristic vector
        
        First come the observing profile values, then the generator values
        """
        charPositionVec = []
        charObsBias = (self.surv.profile.vCharBias
                      +self.surv.profile.oCharBias
                      +self.surv.profile.hCharBias
                      +self.surv.profile.sCharBias)
        charGenBias = self.surv.generator.charBias        
        
        charPositionVec += charObsBias
        for i in range(len(charGenBias)):
            for k in range(len(charGenBias[i])):
                charPositionVec += [charGenBias[i][k]]
        
        
        return charPositionVec


    