"""
Object that generates TransientEvent objects

The purpose of this object is to handle generating
events between frames of TransientSurvey
"""

import numpy as np

class TransientGenerator:
    """
    """

    def __init__(self, surveyShape, generatorFunctions, extraArgs):
        """
        Args:
            surveyShape:
                Tuple: The pixel dimensions of the survey area given
                    by imageArray.shape
                generatorFunction: List of Functions used to make
                    new events. Each function must take in 
                    currentFrameNumber and surveyShape  as their 
                    first two arguments (in that order).
                    These functions must return lists of
                    TransientEvent objects
                extraArgs: List of lists. The ith element in extraArgs
                    is the extra arguments passed to the ith function
                    in generatorFunctions
        """
        self.surveyShape = surveyShape
        self.generatorFunctions = generatorFunctions
        self.extraArgs = extraArgs

    def generate(self, currentFrameNumber):
        newEvents = []
        for i in range(len(self.generatorFunctions)):
            newEvents += self.generatorFunctions[i](
                                    currentFrameNumber, 
                                    self.surveyShape, 
                                    *self.extraArgs[i])
        return newEvents
        