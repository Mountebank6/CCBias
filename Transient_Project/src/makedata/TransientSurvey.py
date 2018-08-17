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
            frameDetectionFunctionList:
                list of frame-detection functions. One function
                for each classID.
                takes as args (TransientEvent object) and 
                returns True if it's detected at the most recent
                frame and returns False if not. If True,
                runs event.recordDetection, which dumps
                current event telemetry to the 
                event.detectionHistory
            holisticDetectionFunctionList:
                list of holistic-detection functions. One function
                for each classID
                Takes as args (TransientEvent object)
                Looks at its history (including when it was 
                frame-detected) and returns True if the event
                as a whole was detected and False otherwise
    """

    def __init__(self, shape, generator, surveyNoiseFunction,
                 frameDetectionFunctionList, 
                 holisticDetectionFunctionList, ):
        self.generator = generator
        self.frameFuncs = frameDetectionFunctionList
        self.holisticFuncs = holisticDetectionFunctionList
        self.shape = shape
        self.surveyNoise = surveyNoiseFunction
        self.events = []
        self.absoluteTime = 0
        self.gen = self.generator.generate

    def advance(self):
        self.absoluteTime += 1
        for event in self.events:
            event.advanceEvent()
        self.events.append(self.gen(self.absoluteTime))
        for event in self.events:
            if self.frameFuncs[event.classID](event):
                event.recordDetection()

    def getHolisticDetecedEvents(self):
        detectedEvents = []
        for event in self.events:
            if self.holisticFuncs[event.classID](event):
                detectedEvents.append(event)
        return detectedEvents


