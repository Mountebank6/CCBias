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
                 popSize, mutRate, crossRate, totalGenerations):
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
            totalGenerations:
                number of times to breed: i.e. number of iterations
                of the *genetic algorithm* you want to run
        
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
        self.totalGenerations = totalGenerations
        
        #Ensure that popsize is divisible by 4
        #This is because the structure of our
        #population-level breeding algorithm requires it
        self.popSize = popSize
        if self.popSize % 4 > 0:
            self.popSize += (4 - self.popSize%4)
        
        self.charGenome = (self.vChar
                         + self.oChar
                         + self.hChar
                         + self.sChar)
        self.genomeLength = len(self.charGenome)
        self.population = self.getRandomPopulation()
        self.scorelist = [1]*len(self.population)

    def runForAllGenerations(self):
        """Run all the iterations of the algorithm and return best genome"""
        for _ in range(self.totalGenerations):
            self.iterate()
        for i in range(self.population):
            if self.scorelist[i] == max(self.scorelist):
                return self.population[i]
    
    def iterate(self):
        """Breed a new generation and score them"""
        
        #Generate a new set of survey data
        #We generate new data each time to reduce
        #overfitting
        self.surv.reRunSurvey(self.runTime)
        
        #Breed the current population and then replace the
        #lower-scoring half with the babies
        pop = self.population
        scores = self.scorelist
        self.population = self.breedPopulation(pop, scores)
        
        #Re score every genome on the new set of survey data
        self.scorelist = []
        for genome in self.population:
            split = self.splitGenome(genome)
            self.surv.setObservingProfileArgs(*split)
            
            newScore = self.score(self.surv)
            self.scorelist.append(newScore)



    def getRandomGenome(self):
        """Return a random genome from the characteristic genome"""
        genome = []
        for cG in self.charGenome:
            if cG[2].lower().strip() == "int":
                genome.append(np.random.randint(cG[0], cG[1]))
            elif cG[2].lower().strip() == "float":
                genome.append(np.random.uniform(cG[0], cG[1]))
            else:
                raise ValueError("characteristicGene[2] neither "
                                + "'int' nor 'float' ")
        return genome
    
    def getRandomPopulation(self):
        """Return a population of random genomes"""
        pop = []
        for _ in range(self.popSize):
            pop.append(self.getRandomGenome)
        return pop
    
    def mutate(self, characteristicGene):
        """Return random legal value for a given gene
        
        Args:
            CharacteristicGene
                A 3-tuple of (low, high, type). type is
                a string, either "int" or "float". and 
                low/high are the inclusive/exclusive bounds on """
        cG = characteristicGene
        if cG[2].lower().strip() == "int":
            return np.random.randint(cG[0], cG[1])
        elif cG[2].lower().strip() == "float":
            return np.random.uniform(cG[0], cG[1])
        else:
            raise ValueError("characteristicGene[2] neither "
                              + "'int' nor 'float' ")


    def splitGenome(self, genome):
        """Return list of extraArgs"""
        #Define borders
        vlen = len(self.vChar)
        olen = len(self.oChar)
        hlen = len(self.hChar)

        #Apply borders
        vArgs = genome[:vlen]
        oArgs = genome[vlen : vlen+olen]
        hArgs = genome[vlen+olen : vlen+olen+hlen]
        sArgs = genome[vlen+olen+hlen:]

        #return in a recognizable format
        return [vArgs, oArgs, hArgs, sArgs]

    
    def breed(self, mother, father):
        """Return child-genomes from crossover and mutation
        
        Args:
            mother/father: 
                Lists of numbers. genomes of the two parents. 
            characteristicGenome:
                List of 3-tuples of the form (low, high, type). 
                The ith 3-tuple in this list represents
                the values and types that the
                ith gene in the child genomes can take on.
                The 'type' is either 'float' or 'int' depending
                on whether fractional values are supported.
                The selection is inclusive on low and exclusive on 
                high
        
        Returns: Length 2 List of child-genomes        
        """
        cG = self.charGenome
        
        #apologies for heteronormativity
        if len(mother) != len(father):
            raise IndexError("Genome lengths mismatched")
        
        #Get number of crossovers and mutations to be applied
        crossovers = binomial(len(mother), self.crossRate)
        mutations = binomial(len(mother), self.mutRate)

        #Get where in the genome they occur
            #here we're choosing that all locations in the genome
            #are equally probable locations for mutation/crossover
        #The use of geneNumbers is for readability
        geneNumbers = range(self.genomeLength)
        
        #Get where in the genome the crossover will occur
        #Sort the locations for iteration further on
        crossLocations = sample(geneNumbers, crossovers)
        crossLocations.sort()
        
        #Use copies to prevent editing the actual parents
        altmother = copy(mother)
        altfather = copy(father)
        
        #Produce two children who are "inverses" of each other
        child1 = [0] * len(altmother)
        child2 = [0] * len(altfather)
        for i in range(crossovers):
            if i % 2 == 0:
                child1[i:] = altfather[i:]
                child2[i:] = altmother[i:]
            else:
                child1[i:] = altmother[i:]
                child2[i:] = altfather[i:]

        #Find where the child genomes mutate
        mutationLocations1 = sample(geneNumbers, mutations)
        mutationLocations1.sort()

        mutationLocations2 = sample(geneNumbers, mutations)
        mutationLocations2.sort()

        #Apply mutations
        for location in mutationLocations1:
            child1[location] = self.mutate(cG[location])

        for location in mutationLocations2:
            child2[location] = self.mutate(cG[location])

        return [child1, child2]
    
    def getSelection(self, probList):
        """Return a selection from a 'cdf' probList"""
        rand = np.random.rand()
        selection = None
        for i in range(len(probList)):
            if probList[i] > rand and selection is None:
                selection = i
        return selection
    
    def rouletteSelect(self, population, scorelist):
        """Return a pair of parents from weighted random selection
        
        Args:
            population:
                list of genomes that were scored in the last round
            
            scorelist:
                List of ints. The ith int is the score of the ith
                genome in population

        Returns:
            mother, father:
                indexes of mother and father genome
                
        """
        totalFitness = np.sum(scorelist)
        sumProbability = 0
        probs = []
        
        for fitness in scorelist:
            #Demarkate the borders by which a random number
            #uniformly drawn in [0,1) is converted to 
            #a selection
            #This is done using the getSelection function
            fitProb = sumProbability + fitness/totalFitness
            probs.append(fitProb)
            sumProbability = probs[-1]
        
        #Use the borders to get the parents
        mother, father = self.getSelection(probs), self.getSelection(probs)
        
        #Check for erros
        if mother is None or father is None:
            raise ValueError("No probability was high enough")

        #Ensure the pair is different
        pathologicalScore = 0
        while mother == father:
            father = self.getSelection(probs)
            pathologicalScore += 1
            if pathologicalScore > 100:
                raise ValueError("mother == father and can't escape")
            
        return [mother, father]

    def breedPopulation(self, population, scorelist):
        """Return new population after weighted breeding"""
        
        numGenome = len(population)
        
        #here we ensure the popsize is divisible by 4.
        #This is because we replace half the population with
        #breeded children, and the breed function returns children
        #pairs. So to produce half of the population using pairs,
        #the population must be divisible by 4
        if numGenome % 4 > 0:
            numGenome += (4 - numGenome%4)
        
        babies = []
        for _ in range(numGenome/4):
            #Select parents from the roulette
            parents = self.rouletteSelect(population, scorelist)
            
            #Make a pair of children fr
            babies += self.breed(*parents)

        newPop = population[:numGenome/2] + babies

        return newPop