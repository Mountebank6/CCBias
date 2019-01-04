"""
Simultaneous Perterbation Stochastic Approximation implementation
for bias analysis
"""
import numpy as np
from copy import deepcopy

class TransientSPSA:


    def __init__(self, blackBox, Q, startingVec, alpha, gamma):
        self.bb = blackBox
        self.Q = Q
        self.r0 = np.asarray(startingVec)
        self.alpha = alpha
        self.gamma = gamma
        self.dim = len(startingVec)

    def a(self,n):
        return 1/(1+n)**self.alpha

    def delta(self,n):
        return 1/(1+n)**self.gamma

    def fixScaledVec(self, scaledVec):
        alt 
        for i in range(len(scaledVec)):
            if np.abs(scaledVec[i]) > 1:
                scaledVec[i] = np.sign(scaledVec[i])

    def bernoulli(self, N):
        bern = np.random.choice([-1/2,1/2], N)
        return bern

    def minimize(self):
        """Return minimized raw parameters"""
        self.iterations = 0
        r = deepcopy(self.r0)
        for i in range(Q):
            bern = self.bernoulli(self.dim)
            a = self.a(i)
            delta = self.delta(i)
            rplus = self.r + delta*bern
            self.fixScaledVec(rplus)
            rminus = r - delta*bern
            self.fixScaledVec(rminus)
            
            Yplus = blackBox.returnValue(rplus)
            Yminus = blackBox.returnValue(rminus)

            for k in range(len(r)):
                r[k] -= a*(Yplus-Yminus)/(2*delta*bern[k])
        return r
            