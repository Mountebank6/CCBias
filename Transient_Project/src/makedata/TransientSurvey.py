"""
Top level class that handles the generation of the survey data
"""

import numpy as np
import copy

class TransientSurvey:
    """
    Args:
        shape:
            length, width of survey area in 2-tuple
        generator:
            TransientGenerator objects which makes the
                events
            surveyNoiseFunction:
                Function that generates noise on the events
                    to simulate ambient sky noise
                    takes as args (event.loc, event.classID)
    """

    def __init__(self, shape, generator, surveyNoiseFunction):
        self.generator = generator 
        self.shape = shape
        self.surveyNoise = surveyNoiseFunction
        self.events = []
        self.absoluteTime = 0
        self.gen = self.generator.generate

    def advance(self):
        """
        Advance the simulation by one frame
        """
        #tick existing things
        self.absoluteTime += 1
        for event in self.events:
            event.advanceEvent()
        #generate new events
        self.events.append(self.gen(self.absoluteTime))

    def getHolisticDetectedEvents(self):
        """Return holistic detected events
        """
        detectedEvents = []
        for event in self.events:
            if event.holisticDetection:
                detectedEvents.append(event)
        return detectedEvents


