from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import astropy.io.fits as fits
import matplotlib.cm as cm
import os
from scipy import stats
from astropy.wcs import WCS
import matplotlib.colors
print(123)


files = os.listdir('/home/user/spxrxs/SupernovaImaging/lcogtdata-20170725-42')
print(files)

hdu1 = fits.open('/home/user/spxrxs/SupernovaImaging/lcogtdata-20170725-42/' + files[1])[1]
hdu2 = fits.open('/home/user/spxrxs/SupernovaImaging/lcogtdata-20170725-42/' + files[12])[1]


plt.figure()
ax1 = plt.subplot(1,2,1, projection=WCS(hdu1.header))

normalised =hdu1.data /stats.trim_mean(hdu1.data, 0.15, axis = None)
sigma = np.sqrt(np.var(normalised))
final_data = np.clip(normalised,np.mean(normalised) - (0.05*sigma), np.mean(normalised) + (5*sigma))
ax1.imshow(np.log(final_data), origin='lower', aspect = 'auto', norm =matplotlib.colors.Normalize() , cmap = cm.bone )
ax1.coords.grid()
ax1.coords['ra'].set_axislabel('Right Ascension')
ax1.coords['dec'].set_axislabel('Declination')
ax1.set_title(hdu1.header['FILTER'])

ax2 = plt.subplot(1,2,2, projection=WCS(hdu2.header))
ax2.imshow(np.log(hdu2.data), origin='lower', aspect = 'auto', norm =matplotlib.colors.Normalize() , cmap = cm.bone)
ax2.coords.grid()
ax2.coords['ra'].set_axislabel('Right Ascension')
ax2.coords['dec'].set_axislabel('Declination')
ax2.set_title(hdu2.header['FILTER'])

plt.show()


from reproject import reproject_interp
array, footprint = reproject_interp(hdu2, hdu1.header)

plt.figure()
ax1 = plt.subplot(1,2,1, projection=WCS(hdu1.header))
ax1.imshow(np.log(array), origin='lower', aspect = 'auto', norm =matplotlib.colors.Normalize() , cmap = cm.bone )
ax1.coords.grid()
ax1.coords['ra'].set_axislabel('Right Ascension')
ax1.coords['dec'].set_axislabel('Declination')
ax1.set_title(hdu1.header['FILTER'])

ax2 = plt.subplot(1,2,2, projection=WCS(hdu1.header))
ax2.imshow(footprint, origin='lower', aspect = 'auto', norm =matplotlib.colors.Normalize() , cmap = cm.bone)
ax2.coords.grid()
ax2.coords['ra'].set_axislabel('Right Ascension')
ax2.coords['dec'].set_axislabel('Declination')
ax2.set_title(hdu2.header['FILTER'])

plt.show()

