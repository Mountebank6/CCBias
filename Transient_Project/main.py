'''
Created on Feb 18, 2018

@author: Theo
'''

if __name__ == '__main__':
    pass

import numpy as np
import makedata.TransientSeries as trans
import makedata.tools.FOV as fov
import imageio as img

number = 500
shap = (500,500)
mean = 30
sigm = 20

gray = trans.TransientSeries(shape=shap,dt=1,n=number,
                            rate=0.00002,lifetime=mean,lifetime_sigma=sigm,             
                            unifv=7, data_type=np.uint8)

bigdata = np.zeros((number,shap[0],shap[1],4), dtype=np.uint8)
#bigdatacovered = np.zeros((number,shap[0],shap[1],4), dtype=np.uint8)
for n in range(number):
    for i in range(len(gray.get_cur_locs())):
        if (gray.get_cur_locs()[i][0] in range(shap[0]) 
                and gray.get_cur_locs()[i][1] in range(shap[1])):
            loc = gray.get_cur_locs()[i]
            if (
                    gray.get_cur_durations()[i] 
                    + gray.get_current_time() 
                    - gray.get_cur_births()[i]) > mean + sigm:
                ass = bigdata[n][gray.get_cur_locs()[i]]
                bigdata[n][loc[0]][loc[1]] = [0,255,0,255]
            else:
                bigdata[n][loc[0]][loc[1]] = [255,255,255,255]
    gray.advance(None)
print("entering gifmaking")
img.mimwrite('uncovered.gif',format = 'gif-pil', 
             ims = bigdata, fps = 30)
#TODO make this make sense
print("gif1 done")
for i in range(len(bigdata)):
    bigdata[i] = fov.apply_dynamic_img_scatter(bigdata[i], 0.85)

print("making final gif")    
img.mimwrite('covered.gif',format = 'gif-pil', 
             ims = bigdata, fps = 30)