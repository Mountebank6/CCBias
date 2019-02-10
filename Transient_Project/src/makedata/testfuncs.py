"""
Library of functions used for testing the stuff
"""

import numpy as np
from src.makedata.TransientEvent import TransientEvent


trans = TransientEvent

def circleView(time, events, radius, center):
    """Return events that are in a circle"""
    passedEvents = []
    for event in events:
        if ((center[0] - event.history[-1][1])**2
           +(center[1] - event.history[-1][2])**2) < radius**2:
           passedEvents.append(event)
    return passedEvents

def allView(time, events):
    """Return all events"""
    return events

def manyArgFunc(a,b,c,d,e,f,g,h,i,j,k,l):
    return

def rectangleView(time, events, size, corner):
    passedEvents = []
    for event in events:
        loc = event.history[-1]
        if loc[1] >= corner[0]:
            if loc[1] <= corner[0] + size[0]:
                if loc[2] >= corner[1]:
                    if loc[2] <= corner[0] + size[1]:
                        passedEvents.append(event)
    return passedEvents

def randomObstruction(time, events, obstructProbability):
    """Return passFraction of events at random"""
    passedEvents = []
    for event in events:
        if np.random.rand() > obstructProbability:
            passedEvents.append(event)
    return passedEvents

def oneFrameDetectHolistic(event):
    """Return True if event was detected even once"""
    if len(event.detectionHistory) > 0:
        return True
    else:
        return False

def gaussSurveyNoise(event, mean, std):
    return np.random.normal(mean, std)

def gaussEventNoise(mean, std):
    return np.random.normal(mean, std)

def genEventsUniform(frame, shape, prob):
    """Generate events with uniform prob over the region
    
    Events have a lifetime of 20 frame with std dev of 5
    events have no luminosity noise and always output at 1
    """
    boxes = shape[0]*shape[1]
    numEvents = np.random.binomial(boxes, prob)
    newEvents = []
    for _ in range(numEvents):
        birth = (np.random.randint(0,shape[0]),
                 np.random.randint(0,shape[1]))
        birthloc = [frame, birth[0], birth[1], 0, 0]
        life = np.random.normal(20,5)
        event = trans(birthloc, life, 5)
        newEvents.append(event)
    return newEvents

