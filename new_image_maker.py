# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 15:07:20 2017

@author: spxrxs
"""

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import astropy.io.fits as fits
import matplotlib.cm as cm
import os
import matplotlib.ticker as ticker
from astropy.wcs import WCS
import matplotlib.colors
from reproject import reproject_interp
from astroscrappy import detect_cosmics

#getting list of every file in the directory
files = os.listdir('/home/user/spxrxs/SupernovaImaging/lcogtdata-20170802-80')
print(files)

#loading the data for plotting
data = np.loadtxt('sn2017ahndata.csv', delimiter = ',', dtype = object)

#opening the FITS file whilch all imaags are aligned to 
hdu1 = fits.open('/home/user/spxrxs/SupernovaImaging/lcogtdata-20170802-80/' + 'coj0m403-kb98-20170302-0140-e91.fits.fz')[1]

#loops through every file in teh folder
for i in range(len(files)):
        
    #opening the file for plotting
    hdu2 = fits.open('/home/user/spxrxs/SupernovaImaging/lcogtdata-20170802-80/' + files[i])[1]
    thing, hdu2.data = detect_cosmics(hdu2.data, readnoise=20., gain=1.4, sigclip=5., sigfrac=.5, objlim=6.)    
    
    
    times = np.zeros(np.shape(data)[0])
    mags = np.zeros(np.shape(data)[0])
    dmags = np.zeros(np.shape(data)[0])    
    
    k = 0
    for j in range(np.shape(data)[0]):
        if hdu2.header['FILTER'] == data[j,1]:
            if hdu2.header['MJD-OBS'] >= float(data[j,0]):
                times[k] = float(data[j,0])
                mags[k] = float(data[j,4])
                dmags[k] = float(data[j,3])
                k +=1
        j +=1
    times = times[:k]
    mags = mags[:k]
    dmags = dmags[:k] 
    
    array, footprint = reproject_interp(hdu2, hdu1.header)
    
    
    plt.figure()
    
    ax1 = plt.subplot2grid((3,3), (0,0), rowspan = 2, colspan = 3)
    #ax1 = plt.subplot(2,1,1, projection = WCS(hdu1.header))
    
    normalised = np.clip(array, np.nanpercentile(array, 50), np.nanpercentile(array, 99.5)) / np.nanpercentile(array, 40)
#    normalised =array /np.nanpercentile(array, 25)
#    sigma = np.sqrt(np.var(normalised))
#    final_data = np.clip(normalised - np.nanpercentile(normalised, 25), 1,4)
    ax1.imshow(np.log(normalised)[200:800,400:1200],  norm =matplotlib.colors.Normalize() , cmap = cm.bone )
    ax1.spines['right'].set_color('none')
    ax1.spines['left'].set_color('none')
    ax1.yaxis.set_major_locator(ticker.NullLocator())
    ax1.xaxis.set_major_locator(ticker.NullLocator())
    #ax1.coords.grid()
    #ax1.coords['ra'].set_axislabel('Right Ascension')
    #ax1.coords['dec'].set_axislabel('Declination')
    #ax1.set_title(hdu2.header['FILTER']+ ' ' + str(hdu2.header['MJD-OBS']))
    
    
    ax2 = plt.subplot2grid((3,3), (2,0), rowspan = 1, colspan = 3)
    plt.errorbar(times -57790, mags, yerr = dmags, fmt = 'o', color = 'red')
    plt.gca().invert_yaxis()
    plt.ylim([21,12]) 
    plt.xlim([0, 100])
    plt.xlabel('Time (Days)')
    plt.ylabel('Magnitude')    
    plt.tight_layout()
    #plt.show()
    i +=1
    print(i)
    plt.savefig(hdu2.header['FIlTER'] + str(hdu2.header['MJD-OBS']) + 'final' +'.png')





