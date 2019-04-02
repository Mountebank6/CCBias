"""
Library of functions used for testing the stuff
"""

import numpy as np
from src.makedata.TransientEvent import TransientEvent


trans = TransientEvent

def circleView(time, frameEvents, radius, center):
    """Return events that are in a circle"""
    passedFrameEvents = []
    for pair in frameEvents:
        if ((center[0] - pair[0].history[-1][1])**2
           +(center[1] - pair[0].history[-1][2])**2) < radius**2:
           passedFrameEvents.append(pair)
    return passedFrameEvents

def allView(time, frameEvents):
    """Return all frameEvents"""
    return frameEvents

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

def getPointInRing(minRad, maxRad):
    """Return a point in the ring from minRad to maxRad inclusive"""
    length = np.sqrt(np.random.uniform(minRad**2, maxRad**2))
    angle = np.pi*np.random.uniform(0,2)
    x = length * np.cos(angle)
    y = length * np.sin(angle)
    return (x,y)

def genLightBugs(frame, shape, surv, bugStart0, bugStart1, bugStart2,
                 birdStart0, birdStart1, birdStart2, 
                 a, c, alpha, gamma):
    #we steal from https://math.psu.edu/tseng/class/Math251/Notes-Predator-Prey.pdf
    #but we modify it for our 3 zones: the predators like the center
    #a, c, alpha, gamma all positive
    radius = int(shape[0]/2)
    if frame == 0:
        #These are lists for the 3 zones [inner, middle, outer]
        surv.bug = [bugStart0, bugStart1, bugStart2]
        surv.bird = [birdStart0, birdStart1, birdStart2]
        surv.areas = [round(np.pi*(radius/3)**2), 
                      round(np.pi*(2*radius/3)**2 - np.pi*(radius/3)**2),
                      round(np.pi*(3*radius/3)**2 - np.pi*(2*radius/3)**2)]
    pBug = [a*surv.bug[0] - alpha*surv.bug[0]*surv.bird[0],
            a*surv.bug[1] - alpha*surv.bug[1]*surv.bird[1],
            a*surv.bug[2] - alpha*surv.bug[2]*surv.bird[2]]
        #Now we make the birds more robust to starvation in the center
    pBird = [-c*(1/6)*surv.bird[0] + gamma*surv.bug[0]*surv.bird[0],
             -c*(3/6)*surv.bird[1] + gamma*surv.bug[1]*surv.bird[1],
             -c*(5/6)*surv.bird[2] + gamma*surv.bug[2]*surv.bird[2]]
    for i in range(len(surv.areas)):
        surv.bug[i] = np.random.binomial(surv.areas[i], pBug[i])
        surv.bird[i] = np.random.binomial(surv.areas[i], pBird[i])

    newEvents = []
    for i in range(len(surv.bug)):
        for _ in range(surv.bug[i]):
            loc = getPointInRing(round(i*radius/3),round((i+1)*radius/3))
            birth = [frame, loc[0], loc[1], 0, 0]
            newEvent = TransientEvent(birth, lifetime = 1, classID = "Bug") 
            newEvents.append(newEvent)

    return newEvents