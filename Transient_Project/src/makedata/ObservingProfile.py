"""
Class to encode the observing profile as well
as detection thresholds

From a conceptual point of view, the Observing Profile plays a 
critical role in the functioning of CCBias. After the synthetic
truth-data is generated, the Observing Profile (OP), dependent on its 
parameters, filters out the data that the OP determines the observer
failed to detect. 
"""

import numpy as np
import copy

OP_REQD_ARGS = {"viewingField" : 3,
                "extraObstruction": 3,
                "holisticDetection": 1,
                "surveyNoiseFunction": 2,
                "measurementFunction": 2}

class ObservingProfile:
    def __init__(self, 
                 viewingField, viewingFieldArgs, vFieldCharPath,
                 vFieldCharBias,

                 extraObstruction, extraObstructionArgs, obstructCharPath,
                 obstructCharBias,

                 holisticDetection, holisticDetectionArgs, hDetectCharPath,
                 hDetectCharBias,

                 surveyNoiseFunction, surveyNoiseFunctionArgs, sNoiseCharPath,
                 sNoiseCharBias,

                 measurementFunction):
        """
        Args:
            viewingField:
                Function. Return an array of events following the FrameEvents
                    convention. The viewingField should look at the events
                    in the FrameEvents input and remove the events that 
                    have inappropriate location.

                    Example: If the observer is a telescope, the viewingField
                    function might remove all events outside the field of
                    view of the telescope.

                    Args: 
                        Time: the time in frames since the 
                        start of the survey

                        FrameEvents: the current FrameEvents (see
                            TransientSurvey for FrameEvents convention)

                        survey: the survey object that holds the events

                        *extraArgs: extra arguments
            extraObstruction:
                Function. Return an array of events following the FrameEvents
                    convention. The extraObstruction should look at the events
                    in the FrameEvents input and remove events for reasons
                    *other* than location data.

                    Example: If events were only detectable beyond some
                    luminosity/intensity threshold, extraObstruction would
                    filter out all events below that threshold.

                    Args: 
                        Time: the time in frames since the 
                        start of the survey

                        FrameEvents: the list of events that exist

                        survey: the relevant survey object itself

            holisticDetection:
                Function. Look at an event's detectionHistory and return true 
                    if the input event is a confirmed detection. 
                    Otherwise returns false.

                    The purpose of holisticDetection is to distinguish
                    between events that are confirmed detections or merely
                    candidate detections. 

                    Args:
                        Event:
                            event to be tested
            surveyNoiseFunction:
                Function that generates noise on the events
                    to simulate ambient sky noise
                    takes as 
                    args: 
                        event
                            the event to have noise generated on
                        survey: the relevant survey object itself
                    returns noise to be added to lum
            vFieldCharPath,eObstructCharPath,hDetectCharPath,sNoiseCharPath:
                Characteristic values for search strategy optimization
                Ranges of legal values for the associated extraArgs.
                each is a list of 3-tuples with lengths equal to
                the lengths of their corresponding extraArgs.
                The tuples tell the range of values over
                which to optimize and the datatype. Of the form:
                (low, high, "float") or (low, high, "int").
                The ranges are inclusive on low, and exclusive on high.
                If the type given is "int", the optimizer will only
                search within integers between low and high.
            vFieldCharBias,eObstructCharBias,hDetectCharBias,sNoiseCharBias:
                Characteristic values for Bias Detection.
                These are the ranges that the Bias extractor will search
                over.
                Ranges of legal values for the associated extraArgs.
                each is a list of 3-tuples with lengths equal to
                the lengths of their corresponding extraArgs.
                The tuples tell the range of values over
                which to optimize and the datatype. Of the form:
                (low, high, "float") or (low, high, "int").
                The ranges are inclusive on low, and exclusive on high.
                If the type given is "int", the optimizer will only
                search within integers between low and high.
            measurementFunction:
                Function. Produces information true and observed event
                    properties.

                The purpose of this function is to compare the
                    observed/true properties of ONE observable at
                    a time. This is because this function does 
                    not return in data where it is possible to
                    associate what data points correspond to
                    the *same* event. e.g. if you have 10 events
                    with a lifetime and a magnitude, you cannot tell
                    what magnitude belonged to the same event as a given
                    luminosity. 
                Args:
                    events:
                        List of all events created
                    survey: 
                        the relevant survey object itself
                Returns:
                    2-tuple of lists of 2-tuples.
                
                The top-level 2-tuple is of the form (true, observed).
                    true is a list of 2-tuples representing data about
                        the true event distribution.
                    observed is a list of 2-tuples representing data
                        about the observed event distribution

                Each 2-tuple inside the lists 'true' and 'observed' is
                    of the form (list, string). The list is data of the
                    events and the string is the name of the parameter
                    measured in the data (e.g. "lifetime)
                
                Example: If there were 3 events generated in total,
                    but only 1 was detected, and we were interested in
                    event lifetime, measurementFunction would return
                    something like;
                        ([([45,23,8],"lifetime")],[([23],"lifetime")])
                    Where the event with lifetime 23 was the only event 
                    to be detected

                        
        """
        self.view = viewingField
        self.vArgs = viewingFieldArgs
        self.vCharPath = vFieldCharPath
        self.vCharBias = vFieldCharBias
        
        self.obstruct = extraObstruction
        self.oArgs = extraObstructionArgs
        self.oCharPath = obstructCharPath
        self.oCharBias = obstructCharBias

        self.holistic = holisticDetection
        self.hArgs = holisticDetectionArgs
        self.hCharPath = hDetectCharPath
        self.hCharBias = hDetectCharBias

        self.surveyNoise = surveyNoiseFunction
        self.sArgs = surveyNoiseFunctionArgs
        self.sCharPath = sNoiseCharPath
        self.sCharBias = sNoiseCharBias
        
        self.measureFunc = measurementFunction

    def frameDetect(self, time, frameEvents, survey):
        """Mark events that are viewed and unobstructed
        """
        #Get the events that are "in frame" as it were
            #at the given absoluteTime
        eventsInView = self.view(time, frameEvents, survey, *self.vArgs)

        #Apply Obstruction to the "in frame" events 
            #at the given absoluteTime
        #The result is all events that have data logged
        frameDetected = self.obstruct(time, eventsInView, 
                                      survey, *self.oArgs)

        
        for pair in frameDetected:
            #pair = (event, index)
            #index is the corresponding index for event.history
            noise = self.surveyNoise(pair[0], survey, *self.sArgs)
            pair[0].recordDetection(pair[1], noise)


        
    def holisticDetect(self, events, survey):
        """Mark events that are detected overall
        """
        for event in events:
            if self.holistic(event, survey, *self.hArgs):
                event.holisticDetection = True
            else:
                event.holisticDetection = False
    