from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import astropy.io.fits as fits
import matplotlib.cm as cm
import os
from scipy import stats
from astropy.wcs import WCS
print(123)


files = os.listdir('H:\My Documents\Supernova\lcogtdata-20170725-42')
print(files)

for i in range(len(files)):  
    hdulist = fits.open('H:\My Documents\Supernova\lcogtdata-20170725-42\\' + files[25])
    print(i/len(files))
    #print(hdulist[0].header)
    #time_array[i] = files[i]{}
    if 1 == 1:
        data = hdulist[1].data
        normalised = data /stats.trim_mean(data, 0.1, axis = None)
        plt.figure()
        plt.subplot(1,1,1,  projection = WCS(hdulist[1].header))
        im = plt.imshow(normalised, cmap = cm.bone, aspect = 'auto', origin = 'Lower')
        plt.colorbar(im)
        plt.show()
##        x = input('What is the X coordinate of the galaxy center?')
##        y = input('What is the Y coordinate of the galaxy center?')
##
##        new_data = normalised[y-250:y+250,x-250:x+250]
##        print(new_data)
##        plt.figure()
##        im2 = plt.imshow(np.log(new_data), cmap = cm.bone, aspect = 'auto', vmin = -2, vmax = 6)
##        #plt.colorbar(im2)
##        plt.savefig(hdulist[1].header['FIlTER'] + str(hdulist[1].header['MJD-OBS']) +'.png')
##        plt.show()
    i +=1
