# -*- coding: utf-8 -*-
"""
Code for aligning images of a given target (Supernova) and plotting the alligned images allong
with a given dataset for teh purpose of creating a short video clip.
Created Ronan Smith 
"""

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import astropy.io.fits as fits
import matplotlib.cm as cm
import os
import matplotlib.ticker as ticker
import matplotlib.colors
from reproject import reproject_interp
from astroscrappy import detect_cosmics
import matplotlib.gridspec as gridspec

def make_images(directory, image_to_allign_to, data_to_plot = None):
    '''Takes 3 inputs:
    directory - the folder in which the datafiles and images are all stored
    image_to_allign_to - the image which every files is alligned
    data_to_plot - the data which is plotted below'''

    #getting list of every file in the directory
    files = os.listdir(directory)
    print(files)
    
    #loading the data for plotting
    if data_to_plot is not None:
        data = np.loadtxt(data_to_plot, delimiter = ',', dtype = object)
    
    #opening the FITS file whilch all imaags are aligned to 
    hdu1 = fits.open(directory + image_to_allign_to)[1]
    
    #loops through every file in teh folder
    for i in range(len(files)):
            
        #opening the file for plotting
        hdu2 = fits.open(directory + files[i])[1]
        
        #removes any cosmic ray hits
        thing, hdu2.data = detect_cosmics(hdu2.data, readnoise=20., gain=1.4, sigclip=5., sigfrac=.5, objlim=6.)    
        
        #finding all data in the file with a date before the date the image was taken
        if data_to_plot is not None:
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
        
        #alligning teh image to same axis as teh 'image_to_allign_to;
        array, footprint = reproject_interp(hdu2, hdu1.header)
            
        #plottingthe data
        
        plt.figure()  
       
        ax1 = plt.subplot2grid((4,1), (0,0), rowspan = 3)
        
        #normalising the data'sn2017ahndata.csv'
        #makes lowest 50% of values equal, to have a nice sky
        #clips top 0.5% to stop peaks/dead pixels ruining teh scale
        #divides by the 40th percentile to make sky value approx 1 (40 seeems to wrok )
        normalised = np.clip(array, np.nanpercentile(array, 60), np.nanpercentile(array, 99.5)) / np.nanpercentile(array, 60)
        
        
        ax1.imshow(np.log(normalised)[200:800,400:1200],   norm =matplotlib.colors.Normalize() , cmap = cm.bone, extent = [0, 100, 0, 75] )
        ax1.spines['right'].set_color('none')
        ax1.spines['left'].set_color('none')
        ax1.yaxis.set_major_locator(ticker.NullLocator())
        #ax1.xaxis.set_major_locator(ticker.NullLocator())
            
        if data_to_plot is not  None:
            time_progression = int(hdu2.header['MJD-OBS'] - 57790)
            ax2 = plt.subplot2grid((4,1), (3,0), rowspan = 1, colspan = 1, sharex = ax1)
            
            plt.scatter(times -57790, mags,  marker = 'x', color = 'c')
            ax2.imshow(np.log(normalised)[50:200,200:(200+(12*time_progression))],   norm =matplotlib.colors.Normalize(), aspect = 'auto' , cmap = cm.bone, extent = [0, time_progression, 12, 22] )
            #ax2.xaxis.set_major_locator(ticker.NullLocator())
            #plt.errorbar(times -57790, mags, yerr = dmags, fmt = 'o', color = 'red')
            #plt.gca().invert_yaxis()
            plt.ylim([22,12]) #may need changing if another supernova is used (only set to a fixed number to keep axis scale consistent)
            plt.xlim([0, 100]) #may need changing if  timescale is extended
            plt.xlabel('Time (Days)')
            plt.ylabel('Magnitude')    
            
            plt.setp(ax1.get_xticklabels(), visible=False)
        #plt.tight_layout() #incase of overlapping labels etc
        plt.show()
        
        
        i +=1 
        print(i) #purely to show it's running 
        
        #saving with a sensible filename
        plt.savefig('final2'+ hdu2.header['FIlTER'] + str(hdu2.header['MJD-OBS']) + 'final' +'.png')



if __name__ == '__main__':
    make_images('/home/user/spxrxs/SupernovaImaging/lcogtdata-20170802-80/', 'coj0m403-kb98-20170302-0140-e91.fits.fz', 'sn2017ahndata.csv')

