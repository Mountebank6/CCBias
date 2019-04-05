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

def bugSurveyNoise(event):
    return 0

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
    return [x,y]

def genLightBugs(frame, shape, surv, bugStart0, bugStart1, bugStart2,
                 birdStart0, birdStart1, birdStart2, 
                 a, c, alpha, gamma):
    #requires a square shape
    
    #we steal from https://math.psu.edu/tseng/class/Math251/Notes-Predator-Prey.pdf
    #but we modify it for our 3 zones: the predators like the center
    #a, c, alpha, gamma all positive
    surv.c = c
    radius = int(shape[0]/2)
    if not hasattr(surv, 'bug'):
        #These are lists for the 3 zones [inner, middle, outer]
        surv.bug = [bugStart0, bugStart1, bugStart2]
        surv.bird = [birdStart0, birdStart1, birdStart2]
        surv.areas = [round(np.pi*(radius/3)**2), 
                      round(np.pi*(2*radius/3)**2 - np.pi*(radius/3)**2),
                      round(np.pi*(3*radius/3)**2 - np.pi*(2*radius/3)**2)]
    
    #Note that the value of alpha is unobservable since birds are unobservable
        #
    pBug = [a*surv.bug[0] - alpha*surv.bug[0]*surv.bird[0],
            a*surv.bug[1] - alpha*surv.bug[1]*surv.bird[1],
            a*surv.bug[2] - alpha*surv.bug[2]*surv.bird[2]]
    
        #Now we make the birds more robust to starvation in the center
    pBird = [-c*(1/6)*surv.bird[0] + gamma*surv.bug[0]*surv.bird[0],
             -c*(3/6)*surv.bird[1] + gamma*surv.bug[1]*surv.bird[1],
             -c*(5/6)*surv.bird[2] + gamma*surv.bug[2]*surv.bird[2]]
    for i in range(len(surv.areas)):
        surv.bug[i] = np.random.binomial(surv.areas[i], min(1,pBug[i]))
        surv.bird[i] = np.random.binomial(surv.areas[i], min(1,pBird[i]))

    newEvents = []
    for i in range(len(surv.bug)):
        for _ in range(surv.bug[i]):
            loc = getPointInRing(round(i*radius/3),round((i+1)*radius/3))
            loc[0] += radius    #move the center of the circle to the
            loc[1] += radius    #middle of the survey
            birth = [frame, loc[0], loc[1], 0, 0]
            newEvent = TransientEvent(birth, lifetime = 1, classID = i) 
            newEvents.append(newEvent)

    return newEvents

def viewBugs(time, frameEvents, surv, rad, center):
    """Return frameEvents of bugs visible in a circle around center
    
        Args:
            rad: radius of viewing circle: given as a fraction of island radius
            center: where on the island to view from: 
                given as a fraction of island radius
    """
    passed = []
    shape = surv.generator.surveyShape
    viewCenter = [int((shape[0]/2)*(1 + center)), int(shape[0]/2)]
    for frameEvent in frameEvents:
        bug = frameEvent[0]
        bugLoc = [bug.x, bug.y]
        deltax = bugLoc[0]-viewCenter[0]
        deltay = bugLoc[1]-viewCenter[1]
        if np.sqrt(deltax**2 + deltay**2) <= rad:
            passed.append(frameEvent)           
    return passed

def bugMeasurementFunction(events, surv):
    """Return the number of bugs detected/existed each frame"""
    allDetectionData = ([[[0,0,0] for i in range(len(surv.absoluteTime)+1)]]
                       +[[[0,0,0] for i in range(len(surv.absoluteTime)+1)]])
    for event in events:
        time = event.time
        allDetectionData[1][time][event.classID] += 1
        if event.holisticDetection:
            allDetectionData[0][time][event.classID] += 1
    return allDetectionData

def intersectionArea(d, R, r):
    """Return the area of intersection of two circles.

    The circles have radii R and r, and their centres are separated by d.

    """
    if d <= abs(R-r):
        # One circle is entirely enclosed in the other.
        return np.pi * min(R, r)**2
    if d >= r + R:
        # The circles don't overlap at all.
        return 0
    r2, R2, d2 = r**2, R**2, d**2
    alpha = np.arccos((d2 + r2 - R2) / (2*d*r))
    beta = np.arccos((d2 + R2 - r2) / (2*d*R))
    return ( r2 * alpha + R2 * beta -
             0.5 * (r2 * np.sin(2*alpha) + R2 * np.sin(2*beta))
           )

def calcOverlapAreas(radius, radFrac, centerFrac):
    """Calculate the overlap of the view with the 3 zones"""
    overlaps = [0,0,0]
    d = centerFrac*radius
    rZones = [radius/3,2*radius/3,3*radius/3]
    rView = radFrac*radius
    overlaps[0] = intersectionArea(d, rZones[0], rView)
    overlaps[1] = intersectionArea(d, rZones[1], rView) - overlaps[0]
    overlaps[2] = intersectionArea(d, rZones[2], rView) - overlaps[0] - overlaps[1]
    return overlaps


def bugScoringFunc(surv):
    """Return 1/(deltac)**2 where deltac is the error in estimate of c"""
    score = 0
    birdCoefficients = [1/6,3/6,5/6] #The modifiers to c in each zone
    detectedEvents = surv.getMeasurementData()[0]
    radius = int(surv.generator.surveyShape[0]/2)
    radFrac = surv.profile.viewingFieldArgs[0]
    centerFrac = surv.profile.viewingFieldArgs[1]
    obsAreas = calcOverlapAreas(radius, radFrac, centerFrac)
    if len(detectedEvents) <= 2:
        #With only one or two frame of data, you cannot say anything about dynamics
        #This is because the data from bird lags into propogating to bug
        return 1
    
    A = [] #the matrix which will let us solve for c, a, and gamma in Ax=b
    b = [] #the b vector in Ax=b
    for i in range(len(detectedEvents)-2):
        bugLast = detectedEvents[i]
        bugNext = detectedEvents[i+1]
        bugAfterNext = detectedEvents[i+2]
        for k in range(3):
            if obsAreas[k] > 0:
                A.append([-bugNext[k], -bugNext[k]*birdCoefficients[k], 
                          bugNext[k]**2, -(bugNext[k]**2)/obsAreas[k] ])
                b.append([-bugAfterNext[k]/obsAreas[k]
                          -(bugNext[k]**2)/(obsAreas[k]*bugLast[k])])
    coefficientVector = np.linalg.lstsq(A,b)
    cEstimate = coefficientVector[1]/coefficientVector[0]
    score = max(0,1/(cEstimate-surv.c)**2)        
    return score