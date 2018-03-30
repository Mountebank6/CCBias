'''
Created on Feb 18, 2018

@author: Theo
'''

if __name__ == '__main__':
    pass

import numpy as np
import makedata.TransientSeries as trans
import makedata.tools.FOV as fov
import astropy.io.fits as fit

#gray = trans.TransientSeries(shape=(500,500),dt=1,n=500,
#                            rate=0.00002,lifetime=30,lifetime_sigma=5,
#                            unifv=7,filename="testing")
#gray.advance_to_end()
#print("done")

#look = []
#for k in range(500):
#    look.append((k,k))
#for i in range(500):
#    fly = fit.getdata("testing%s.0.fits" %i)
#    fov.apply_circle_fov(np.uint16, fit.getdata("testing%s.0.fits" %i), 
#                         100, look[i], "spotlight" + str(i))