from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import astropy.io.fits as fits
import matplotlib.cm as cm
import os
from scipy import stats
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
import re


print('Please Select the Directory in which the files are stored')
folder = Tk()
folder.directory = tkFileDialog.askdirectory()
print (folder.directory)
folderstr = str(folder.directory)
folder.quit()
print('Please Select a file to open')
filename = Tk()
filename.filename = tkFileDialog.askopenfile(initialdir = folder ,title = "Select file",filetypes = (("FITS files","*.fits.fz"),("all files","*.*")))
print(filename.filename)
filenamestr = re.split("'",str(filename.filename))[1]
filename.quit()

hdulist = fits.open(filenamestr)
rawdata = hdulist[1].data
data = rawdata /stats.trim_mean(rawdata, 0.1, axis = None)
plt.figure()
im = plt.imshow(np.log(data), cmap = cm.bone, aspect = 'auto' )
plt.colorbar(im)
plt.show()

x = input('What is the X coordinate of the galaxy center?')
y = input('What is the Y coordinate of the galaxy center?')

new_data = data[y-200:y+200,x-200:x+200]
print(new_data)
plt.figure()
im2 = plt.imshow(np.log(new_data), cmap = cm.bone, aspect = 'auto')
plt.colorbar(im2)
plt.show()
          














##
##print(123)
##files = os.listdir('H:\My Documents\Supernova\lcogtdata-20170725-42')
##print(files)
##
##hdulist = fits.open('H:\My Documents\Supernova\lcogtdata-20170725-42\\' + files[i])
##print(i/len(files))
##    #print(hdulist[0].header)
##    #time_array[i] = files[i]{}
##    if hdulist[1].header['FILTER'] == 'V':
##        data = hdulist[1].data
##        normalised = data /stats.trim_mean(data, 0.2, axis = None)
##        plt.figure()
##        plt.suptitle(files[i])        
##        plt.subplot(211)
##        im = plt.imshow(np.log(normalised), cmap = cm.hot, aspect = 'auto')
##        plt.colorbar(im)
##        plt.subplot(212)
##        plt.scatter(np.arange(np.shape(normalised)[1]),np.var(normalised, axis = 0))
##        plt.xlabel(np.argmax(np.var(normalised, axis = 0)))
##    i +=1
##plt.show()

#plt.imshow((hdulist[3].data))
#plt.imshow(np.log(hdulist[1].data/stats.trim_mean(hdulist[1].data, 0.2, axis = None)), cmap =cm.bone)

