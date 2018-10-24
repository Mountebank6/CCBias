"""
Top level class that handles the generation of the survey data
"""

import numpy as np
import copy

class TransientSurvey:
    """
    Args:
        generator:
            TransientGenerator objects which makes the
                events
        profile:
            ObservingProfile object which determines sight
            
    """

    def __init__(self, generator, profile):
        self.generator = generator 
        self.profile = profile
        self.events = []
        self.frameEvents = []
        self.absoluteTime = -1
        self.gen = self.generator.generate

    def advance(self):
        """
        Advance the simulation by one frame
        """
        #tick existing things
        self.absoluteTime += 1
        self.frameEvents.append([])
        for event in self.events:
            event.advanceEvent()
            
            #Record what events are alive in this frame,
            #   and what index in its history this frame is
            if not event.markedForDeath:
                index = len(event.history) - 1
                self.frameEvents[-1].append((event, index))
        
        #Detect the next frame of events.
        #Here we decide to exclude new events from the detection
            #calculus. 
            #i.e. you will never detect the first frame
        if len(self.frameEvents) > 0:
            self.profile.frameDetect(self.absoluteTime, 
                                     self.frameEvents[-1], self)
        
        #generate new events
        self.events += self.gen(self.absoluteTime, self)

    def advanceWithoutDetection(self):
        """Advance the simulation without checking for detection"""
        self.absoluteTime += 1
        self.frameEvents.append([])
        for event in self.events:
            event.advanceEvent()
            if not event.markedForDeath:
                index = len(event.history) - 1
                self.frameEvents[-1].append((event, index))
        self.events += self.gen(self.absoluteTime, self)
    
    def getHolisticDetectedEvents(self):
        """
        Return holistic detected events
        """
        detectedEvents = []
        self.profile.holisticDetect(self.events, self)
        for event in self.events:
            if event.holisticDetection:
                detectedEvents.append(event)
        return detectedEvents

    def getLivingEvents(self):
        """Return list of living events"""
        livers = []
        for event in self.events:
            if not event.markedForDeath:
                livers.append(event)
        return livers

    def getDeadEvents(self):
        """Return list of dead events"""
        corpses = []
        for event in self.events:
            if event.markedForDeath:
                corpses.append(event)
        return corpses

    def resetSurvey(self):
        """Clear events and reset time"""
        self.events = []
        self.frameEvents = []
        self.absoluteTime = -1

    def reDetectEvents(self):
        """Run detection again on all events"""

        #Clear the past profile's detections
        for event in self.events:
            event.clearDetectionHistory()
        
        #Perform frameDetection on entire survey history
        for i in range(self.absoluteTime):
            self.profile.frameDetect(i, self.frameEvents[i], self)

        #Mark Holistically detected events
        self.profile.holisticDetect(self.events, self)
    
    def setObservingProfile(self, newProfile):
        """Change the observing profile and re-detect events

        Args:
            profile:
                The ObservingProfile object to change to.
        """

        #Change the profile
        self.profile = newProfile

        #rerun detection
        self.reDetectEvents()

    def setGeneratorFunctionArgs(self, args):
        self.gen.eargs = args
    
    def setObservingProfileArgs(self, vArgs, oArgs, hArgs, sArgs):
        """Re detect events after changing ObservingProfile's extra args
        
        Args:
            vArgs:
                viewingField extra args. list of parameters
            oArgs:
                extraObstruction extra args. list of parameters
            hArgs:
                holisticDetection extra args. list of parameters
            sArgs:
                surveyNoiseFunction extra args. list of parameters    
        """
        #Swap out the parameters
        self.profile.vArgs = vArgs
        self.profile.oArgs = oArgs
        self.profile.hArgs = hArgs
        self.profile.sArgs = sArgs

        #Re run detection
        self.reDetectEvents()

    def reRunSurvey(self, time=None):
        """Reset the survey and rerun
        
        Args:
            time:
                number of time-steps to rerun for
        """
        if time is None:
            time = self.absoluteTime
        self.resetSurvey()

        for _ in range(time):
            self.advance()

    def getMeasurementData(self):
        return self.profile.measurementFunction(self.events, self)