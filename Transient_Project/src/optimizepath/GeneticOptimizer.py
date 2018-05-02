"""
Use a score function to optimize search path using a genetic algorithm

@author = Theo Faridani
"""

import numpy as np
from collections import namedtuple
from ..makedata import TransientSeries as tr
from .opttools import scoring
from .opttools import searchpath
from ..makedata.tools import FOV

def GeneticOptimizer(generator, crossrate, mutrate, popsize, iterations, 
                     scoring_function, scoring_function_extra_args):
    """Return optimized search paths for a given TransientSeries"""
    genomelength = generator.get_n()
    searchspace = generator.get_shape()
    point = namedtuple("Point", "x y")
    if crossrate > 1 or crossrate < 0:
        raise ValueError("crossrate is of inappropriate value")
    if mutrate > 1 or mutrate < 0:
        raise ValueError("mutrate is of inappropriate value")
    if not isinstance(generator, tr.TransientSeries):
        raise TypeError("generator is not a TransientSeries")
    
    population = []
    for _ in range(popsize):
        genome = []
        for _ in range(genomelength):
            genome.append(point(
                            np.random.randint(0,searchspace[0]-1),
                            np.random.randint(0,searchspace[1]-1)
                          ))
        population.append(genome)
    

    return population