# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 10:18:29 2017

@author: spxrxs
"""

import matplotlib.pyplot as plt
import numpy as np
import astropy.io.fits as fits
import matplotlib.cm as cm
#import os


hdulist = fits.open('H:\My Documents\Supernova\lcogtdata-20170725-42\\coj0m403-kb98-20170403-0101-e91.fits.fz')
print(hdulist[0])
print(hdulist[0].header)
print(hdulist[1].header)
print(hdulist[2].header)
print(hdulist[3].header)

#print(hdulist[2].data)

plt.imshow(np.log(hdulist[3].data)
