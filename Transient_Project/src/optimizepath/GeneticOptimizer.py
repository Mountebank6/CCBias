"""
Use a score function to optimize search path using a genetic algorithm

@author = Theo Faridani
"""

import numpy as np
import random
from collections import namedtuple
from ..makedata import TransientSeries as tr
from .opttools import scoring
from .opttools import searchpath
from ..makedata.tools import FOV
import copy

def GeneticOptimizer(generator_class, generator_args, crossrate, mutrate, 
                     popsize, genetic_iterations, scoring_function, 
                     characterized_genome):
    """Return optimized search paths for a given TransientSeries
    
    Args:
        generator:
            The class that generates the images and event data
        crossrate:
            The probability that a given site on the genome
            is a crossover site
        mutrate:   
            The probability that a given site on the genome
            is a mutation site 
        popsize:
            number of genomes to hold and breed
        genetic_iterations;
            number of iterations of breeding and selecting to do
        scoring_function:
            the function used to score the genomes
        characterized_genome:
            Describes the properties of the components of a single gene
            See genome_characterizer docstring for more details
    """
    generator = generator_class(*generator_args)

    genomelength = generator.get_n()
    if crossrate > 1 or crossrate < 0:
        raise ValueError("crossrate is of inappropriate value")
    if mutrate > 1 or mutrate < 0:
        raise ValueError("mutrate is of inappropriate value")
    population = gen_initial_population(popsize, genomelength, 
                                        characterized_genome)
    #begin scoring
    for generation in range(genetic_iterations):
        scores = [0 for element in population]
        for k in range(genomelength):
#            print("completed an image")
            for i in range(len(population)):
                scores[i] += scoring_function(generator, *population[i][k])
            generator.advance()
        
        generator = generator_class(*generator_args)
        babies = round(popsize/2)
        babypop = []
        for _ in range(babies):
            crossovers = np.random.binomial(genomelength, crossrate)
            mutations = np.random.binomial(genomelength, mutrate)
            babypop.append(breed(*roulette_select(scores, population),
                                crossovers, mutations, characterized_genome))
        population = [genome for _,genome in sorted(zip(scores,population))]
        scores = [score for score,_ in sorted(zip(scores,population))]

        if generation == genetic_iterations - 1:
            return list(reversed(scores)), list(reversed(population))

        for lowscoreindex in reversed(range(babies)):
            del population[lowscoreindex]
        population = list(reversed(population))
        population += babypop
        print("Generation: " + str(generation))
        print(np.mean(scores))
def genome_characterizer(minlist, maxlist, typelist):
    """Return a list with information that characterizes the genome
    
    The returned list is an array that contains all the information
    to construct the genome. For each parameter it gives the data type,
    the minimum, and the maximum value. 

    The inputs must be in the same order as the inputs that the
    scoring function that scores this genome will use.

    Args:
    minlist:
        List of the minimum values that the gene can take
    maxlist:
        List of the maximum values that the gene can take
    typelist:
        List of strings denoting the type of the gene.
        Only float, and int allowed 
        (e.g. "float", "Float", "INT")
    """
    if len(minlist) != len(maxlist) or len(maxlist) != len(typelist):
        raise ValueError("Lists of different lengths")
    typelist = [genetype.lower().strip() for genetype in typelist]
    characterized_genome = []
    for i in range(len(minlist)):
        if typelist[i] == "float":
            characterized_genome.append((
                                    float(minlist[i]), 
                                    float(maxlist[i])
                                        ))
        elif typelist[i] == "int":
            characterized_genome.append((
                                    int(minlist[i]), 
                                    int(maxlist[i])
                                        ))
        else:
            raise TypeError("invalid type in typelist " + str(typelist[i]))
    return characterized_genome

def gen_initial_population(popsize, genomelength, characterized_genome):
    """Return initial population of genomes"""
    population = []
    char = characterized_genome
    for _ in range(popsize):
        gene = [[] for _ in range(genomelength)]
        for i in range(len(char)):
            genecomponent = []
            if isinstance(char[i][0], float):
                for _ in range(genomelength):
                    genecomponent.append([
                        (char[i][1]-char[i][0])*np.random.rand() 
                        + char[i][0]
                                        ])
            elif isinstance(char[i][0], int):
                for _ in range(genomelength):
                    genecomponent.append([
                                        np.random.randint(char[i][0],
                                        char[i][1]+1)
                                        ])
            else:
                raise TypeError("your characteristic genome has bad types")
            for i in range(len(gene)):
                gene[i] += genecomponent[i]
        population.append(gene)
    return population

def breed(mother, father, crossovers, mutations, characterized_genome):
    """Return a crossed-over and mutated child"""
    if len(mother) != len(father):
        raise IndexError("mother and father of different lengths")
    if crossovers > len(mother):
        raise ValueError("More crossovers than genes")
    if mutations > len(mother):
        raise ValueError("More mutations than genes to mutate")
    crossoverlocs = random.sample(range(len(mother)), crossovers)
    crossoverlocs.sort()
    mother2, father2 = copy.deepcopy(mother), copy.deepcopy(father)
    
    if np.random.rand() > 0.5:
        #this is to remove score bias, since the mother is the
        #higher scorer
        mother2, father2 = father2, mother2
    child = mother2
    for i in range(len(crossoverlocs)):
        if i % 2 == 0:
            child[i:] = father2[i:]
        else:
            child[i:] = mother2[i:]
    mutationlocs = random.sample(range(len(mother2)), mutations)
    mutationlocs.sort()
    for loc in mutationlocs:
        innerchange = np.random.randint(0,len(child[loc]))
        child[loc][innerchange] = gen_initial_population(1,1,
                                    characterized_genome)[0][0][innerchange]
    return child

def roulette_select(scorelist, population):
    
    weighted = [[i]*max(1, 1 + scorelist[i]) for i in range(len(scorelist))]
    flatweighted = [item for sublist in weighted for item in sublist]
    selection = np.random.randint(0, len(flatweighted))
    mother = flatweighted[selection]
    
    selection2 = np.random.randint(0, len(flatweighted))
    father = flatweighted[selection2]
    pathological_score = 0

    while mother == father:
        selection2 = np.random.randint(0, len(flatweighted))
        father = flatweighted[selection2]
        pathological_score += 1
        if pathological_score > 10000:
            raise ValueError("mother == father and can't escape")
    
    return [population[mother], population[father]]