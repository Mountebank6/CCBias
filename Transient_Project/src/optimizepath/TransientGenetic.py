import numpy as np
import random
from copy import copy, deepcopy


"""To do this we will require the setup of the
TransientSurvey object to take in ranges for the different
variables. This will allow the construction of the
characterized genome"""

binomial = np.random.binomial
sample = random.sample

class TransientGenetic:
    """Class that optimizes survey score with genetic algorithm"""

    def __init__(self, survey, scoringFunc, surveyTime,
                 popSize, mutRate, crossRate, iterations):
        """
        Args:
            survey:
                The TransientSurvey object to run and reset
                in order to optimize
            scoringFunc:
                Function that takes as its only argument
                    the survey object, and returns a float:
                    the score of the survey. Higher => better
            surveyTime:
                Iterations to run survey before scoring it
        
        """

        self.vChar = deepcopy(survey.profile.vChar)
        self.oChar = deepcopy(survey.profile.oChar)
        self.hChar = deepcopy(survey.profile.hChar)
        self.sChar = deepcopy(survey.profile.sChar)
        self.score = scoringFunc
        self.runTime = surveyTime
        self.surv = survey
        self.crossRate = crossRate
        self.mutRate = mutRate
        self.iterations = iterations
        self.charGenome = (self.vChar
                         + self.oChar
                         + self.hChar
                         + self.sChar)
        self.genomeLength = len(self.charGenome)
        return

    def breed(self, mother, father):
        """Return child-genomes from crossover and mutation"""
        #apologies for heteronormativity
        if len(mother) != len(father):
            raise IndexError("Genome lengths mismatched")
        
        #Get number of crossovers and mutations to be applied
        crossovers = binomial(len(mother), self.crossRate)
        mutations = binomial(len(mother), self.mutRate)

        #Get where in the genome they occur
            #here we're choosing that all locations in the genome
            #are equally probable locations for mutation/crossover
        #The definition of geneNumbers is for readability
        geneNumbers = range(self.genomeLength)
        
        #Get where in the genome the crossover will occur
        #Sort the locations for iteration further on
        crossLocations = sample(geneNumbers, crossovers)
        crossLocations.sort()
        
        child1 = mother
        child2 = father
        for i in range(crossovers):
            if i % 2 == 0:
                child1[i:] = father[i:]
                child2[i:] = mother[i:]
            else:
                child1[i:] = mother[i:]
                child2[i:] = father[i:]


