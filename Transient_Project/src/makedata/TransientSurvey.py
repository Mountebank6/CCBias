"""
Top level class that handles the generation of the survey data
"""

import numpy as np
import copy

class TransientSurvey:
    """
    """

    def __init__(self, shape, generator, surveyNoiseFunction,
                 frameDetectionFunctionList, 
                 holisticDetectionFunctionList, ):
        self.generator = generator
        self.frameFuncs = frameDetectionFunctionList
        self.holisticFuncs = holisticDetectionFunctionList
        self.shape = shape
        self.surveyNoise = surveyNoiseFunction
