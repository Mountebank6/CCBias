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

number = 600
shap = (500,500)
mean = 30
sigm = 20
velo = 0
prob = 0.000002

gray = trans.TransientSeries(shape=shap,dt=1,n=number,
                            rate=prob,lifetime=mean,lifetime_sigma=sigm,             
                            unifv=velo, data_type=np.uint8)

def make_greens_array(transseries):
    final = np.zeros((shap[0],shap[1],4), dtype=np.uint8)
    for i in range(len(transseries.get_cur_locs())):
        if (transseries.get_cur_locs()[i][0] in range(shap[0]) 
                and transseries.get_cur_locs()[i][1] in range(shap[1])):
            loc = transseries.get_cur_locs()[i]
            if (
                    transseries.get_cur_durations()[i] 
                    + transseries.get_current_time() 
                    - transseries.get_cur_births()[i]) > mean + sigm:
                final[loc[0]][loc[1]] = [0,255,0,255]
            else:
                final[loc[0]][loc[1]] = [255,255,255,255]
    return final

bigdata = np.zeros((number,shap[0],shap[1],4), dtype=np.uint8)
#bigdatacovered = np.zeros((number,shap[0],shap[1],4), dtype=np.uint8)
print("entering imagemaking")
for n in range(number):
    bigdata[n] = make_greens_array(gray)
    gray.advance(None)
print("entering gifmaking")

img.mimwrite('uncoveredstilllowp.gif',format = 'gif-pil', 
             ims = bigdata, fps = 30)
#TODO make this make sense
print("gif1 done")

popping_circle = []
locs = []
for n in range(number):
    if n % 30 == 0:
        loc = (np.random.randint(0,shap[0]),
                np.random.randint(0,shap[1]))
    locs.append(loc)

for i in range(len(bigdata)):
    bigdata[i] = fov.apply_circle_fov(bigdata[i],40, locs[i])

print("making final gif")    
img.mimwrite('coveredstilllowp.gif',format = 'gif-pil', 
             ims = bigdata, fps = 30)