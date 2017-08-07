from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import astropy.io.fits as fits
import matplotlib.cm as cm
import os
from scipy import stats

print(123)
files = os.listdir('H:\My Documents\Supernova\lcogtdata-20170725-42')
print(files)

for i in range(len(files)-1):  
    hdulist = fits.open('H:\My Documents\Supernova\lcogtdata-20170725-42\\' + files[i])
    print(i/len(files))
    #print(hdulist[0].header)
    #time_array[i] = files[i]{}
    if hdulist[1].header['FILTER'] == 'V':
        data = hdulist[1].data
        normalised = data /stats.trim_mean(data, 0.2, axis = None)
        plt.figure()
        plt.suptitle(files[i])        
        plt.subplot(211)
        im = plt.imshow(np.log(normalised), cmap = cm.bone, aspect = 'auto', vmin = -2, vmax = 6)
        #plt.colorbar(im)
        plt.subplot(212)
        plt.scatter(np.arange(np.shape(normalised)[1]),np.var(normalised, axis = 0))
        plt.xlabel(np.argmax(np.var(normalised, axis = 0)))
    i +=1
plt.show()

#plt.imshow((hdulist[3].data))
#plt.imshow(np.log(hdulist[1].data/stats.trim_mean(hdulist[1].data, 0.2, axis = None)), cmap =cm.bone)

