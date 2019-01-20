"""
Simultaneous Perterbation Stochastic Approximation implementation
for bias analysis
"""
import numpy as np
from copy import deepcopy

class TransientSPSA:


    def __init__(self, blackBox, Q, startingVec, alpha=1.0, gamma=1.0/6):
        """
        Args: 
            blackBox:
                A TransientBlackBox object. Can be replace with
                any class that has a returnValue method that returns float
            Q:
                Number of iterations to run the SPSA algorithm
            startingVec:
                The vector to start optimization at. Scaled
            alpha:
                a parameter that controls the step size sequence
                must satisfy 
        """
        self.bb = blackBox
        self.Q = Q
        self.r0 = np.asarray(startingVec, dtype=np.float)
        self.alpha = alpha
        self.gamma = gamma
        self.dim = len(startingVec)

    def a(self,n):
        """Return the nth value of the step-size sequence"""
        return 1/(1+n)**self.alpha

    def delta(self,n):
        """Return the nth value of the probing sequence"""
        return 1/(1+n)**self.gamma

    def fixScaledVec(self, scaledVec):
        """Truncate the input vector so that it lies within [-1,1]^dim"""
        for i in range(len(scaledVec)):
            if np.abs(scaledVec[i]) > 1:
                scaledVec[i] = np.sign(scaledVec[i])

    def bernoulli(self, N):
        """Return a bernoulli distributed N-dimensional numpy vector"""
        bern = np.random.choice([-1/2,1/2], N)
        return bern

    def minimize(self):
        """Return minimized raw parameters"""
        self.iterations = 0
        r = deepcopy(self.r0)
        for i in range(self.Q):
            bern = self.bernoulli(self.dim)
            a = self.a(i)
            delta = self.delta(i)
            self.fixScaledVec(r)
            rplus = r + delta*bern
            self.fixScaledVec(rplus)
            rminus = r - delta*bern
            self.fixScaledVec(rminus)
            
            Yplus = self.bb.returnValue(rplus)
            Yminus = self.bb.returnValue(rminus)

            for k in range(len(r)):
                r[k] -= a*(Yplus-Yminus)/(2*delta*bern[k])
            self.fixScaledVec(r)
        return r, self.bb.scaledVecToRawVec(r)
            