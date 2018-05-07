'''
Created on Feb 18, 2018

@author: Theo
'''

if __name__ == '__main__':
    pass

import numpy as np
import src.makedata.TransientSeries as trans
import src.makedata.tools.FOV as fov
import imageio as img
from scipy import special
from scipy import integrate
from math import sqrt, pi, exp
import src.optimizepath.GeneticOptimizer as gen
import src.optimizepath.opttools.scoring as scor
import src.viewdata.drawers as draw

import cProfile
import re

number = 50
shap = (500,500)
mean = 10
sigm = 5
dt = 1
velo = 0
prob = 0.0000002

superbiasedarray = np.zeros(shap)
for i in range(len(superbiasedarray)):
    for k in range(len(superbiasedarray[i])):
        if i < 150 and k < 150:
            superbiasedarray[i][k] = 0.005
#gray = trans.TransientSeries(shap, dt, number, superbiasedarray, mean, sigm)

scores, population = gen.GeneticOptimizer(trans.TransientSeries,[shap, dt, 
                        number, superbiasedarray, mean, sigm], 0.01, 0.00000005,
                        500, 10, scor.int_intensity_square,
                        gen.genome_characterizer([0,0,10], [499,499,10],
                        ["int", "int","int"]))

gray = trans.TransientSeries(shap, dt, number, superbiasedarray, mean, sigm)

bigdata = np.zeros((number,shap[0],shap[1],4), dtype=np.uint8)
print("entering imagemaking")
for n in range(number):
    bigdata[n] = draw.make_greens_array(gray) 
    gray.advance(None)
locs = [[element[0],element[1]] for element in population[0]]
radius = population[0][0][2]
for i in range(len(bigdata)):
    bigdata[i] = fov.apply_square_fov(bigdata[i], radius, locs[i])

img.mimwrite("genetically-optimized.gif",format = 'gif-pil', 
             ims = bigdata, fps = 5)

print(scores)
