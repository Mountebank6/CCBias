"""
Class to encode the observing profile as well
as detection thresholds
"""

import numpy as np
import copy

class ObservingProfile:
    """
    """
    def __init__(self, viewingField, viewingFieldArgs, vFieldChar,
                 extraObstruction, extraObstructionArgs, obstructChar,
                 holisticDetection, holisticDetectionArgs, hDetectChar,
                 surveyNoiseFunction, surveyNoiseFunctionArgs, sNoiseChar):
        """
        Args:
            viewingField:
                Function. Returns a list of events that are 
                potentially observable because the "telescope"
                is pointed at them. This selection should
                be orthogonal to extraObservation
                    Args: 
                        Time: the time in frames since the 
                        start of the survey

                        Events: the list of events that exist
            extraObstruction:
                Function. Returns a list of events that are
                potentially observable because they are not 
                obstructed by anything. This selection
                should be orthogonal to viewingField
                    Args: 
                        Time: the time in frames since the 
                        start of the survey

                        Events: the list of events that exist

            holisticDetection:
                Function. Takes in a single event (generally dead ones,
                but not necessarily) and detirmines if they are "detected"
                If they are, returns True
                    Args:
                        Event:
                            event to be tested
            surveyNoiseFunction:
                Function that generates noise on the events
                    to simulate ambient sky noise
                    takes as args: event
                    returns noise to be added to lum
            vFieldChar, eObstructChar, hDetectChar, sNoiseChar:
                Ranges of legal values for the associated extraArgs.
                each is a list of 3-tuples with lengthsequal to
                the lengths of their corresponding extraArgs.
                The tuples tell the range of values over
                which to optimize and the datatype. Of the form:
                (low, high, "float") or (low, high, "int").
                The ranges are inclusive on low, and exclusive on high.
                If the type given is "int", the optimizer will only
                search within integers between low and high.
            
                        
        """
        self.view = viewingField
        self.vArgs = viewingFieldArgs
        self.vChar = vFieldChar
        self.obstruct = extraObstruction
        self.oArgs = extraObstructionArgs
        self.oChar = obstructChar
        self.holistic = holisticDetection
        self.hArgs = holisticDetectionArgs
        self.hChar = hDetectChar
        self.surveyNoise = surveyNoiseFunction
        self.sArgs = surveyNoiseFunctionArgs
        self.sChar = sNoiseChar

    def frameDetect(self, time, frameEvents):
        """Mark events that are viewed and unobstructed
        """
        #Get the events that are "in frame" as it were
            #at the given absoluteTime
        eventsInView = self.view(time, frameEvents,*self.vArgs)

        #Apply Obstruction to the "in frame" events 
            #at the given absoluteTime
        #The result is all events that have data logged
        frameDetected = self.obstruct(time, eventsInView, *self.oArgs)

        
        for pair in frameDetected:
            #pair = (event, index)
            #index is the corresponding index for event.history
            noise = self.surveyNoise(pair[0], *self.sArgs)
            pair[0].recordDetection(pair[1], noise)


        
    def holisticDetect(self, events):
        """Mark events that are detected overall
        """
        for event in events:
            if self.holistic(event, *self.hArgs):
                event.holisticDetection = True
            else:
                event.holisticDetection = False
    