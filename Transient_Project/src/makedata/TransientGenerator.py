"""
Object that generates TransientEvent objects

The purpose of this object is to handle generating
events between frames of TransientSurvey
"""

import numpy as np

TRANS_REQD_ARGS = {"generatorFunction": 3}

class TransientGenerator:
    """
    """

    def __init__(self, surveyShape, generatorFunctions, extraArgs,
                 genFuncCharBias):
        """
        Args:
            surveyShape:
                Tuple: The pixel dimensions of the survey area
            
            generatorFunction: 
                List of Functions used to make new events.
                    Args: 
                        currentFrameNumber:
                            The current frame of the simulation
                        surveyShape:
                            The pixel dimensions of the survey
                        survey:
                            The survey object itself.                   
                    The logic behind passing in the survey object
                    is so that the generator functions can produce 
                    events that are not independent and identically 
                    distributed. For example, if we wanted to model
                    a unique object (e.g. the moon), the generator
                    functions need to be able to check if that object
                    already exists.
            extraArgs: 
                List of lists. The ith element in extraArgs
                is the extra arguments passed to the ith function
                in generatorFunctions
            genFuncCharBias:
                List of lists of tuples
                    The sublists correspond to the characteristic genomes
                        for the extra args of the associated generator 
                        functions.
                    The i'th element of the sublist is a 2-tuple that
                        defines the min value, then the max value
                        of the ith argument in the generator functions
                        extra args.
                        The ranges are inclusive on min, and inclusive on max
        """
        self.surveyShape = surveyShape
        self.generatorFunctions = generatorFunctions
        self.eArgs = extraArgs
        self.charBias = genFuncCharBias

    def generate(self, currentFrameNumber, survey):
        newEvents = []
        for i in range(len(self.generatorFunctions)):
            newEvents += self.generatorFunctions[i](
                                    currentFrameNumber, 
                                    self.surveyShape, 
                                    survey,
                                    *self.eArgs[i])
        return newEvents
        