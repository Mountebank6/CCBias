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
            
            #Record what events are alive in this frame,
            #   and what index in its history this frame is
            self.frameEvents.append([])
            if not event.markedForDeath:
                index = len(event.history) - 1
                self.frameEvents[-1].append((event, index))
        
        #Detect the next frame of events.
        #Here we decide to exclude new events from the detection
            #calculus
        self.profile.frameDetect(self.absoluteTime, self.events)
        
        #generate new events
        self.events += self.gen(self.absoluteTime)

    def getHolisticDetectedEvents(self):
        """
        Return holistic detected events
        """
        detectedEvents = []
        self.profile.holisticDetect(self.events)
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
        self.absoluteTime = 0

    def setObservingProfile(self, profile):
        """Change the observing profile and re-detect events

        Args:
            profile:
                The ObservingProfile object to change to.
        """

        for event in self.events:
            event.clearDetectionHistory()
        
        #for i in range(self.absoluteTime):
        #    self.profile.frameDetect(i+1, self.frameEvents[i])

