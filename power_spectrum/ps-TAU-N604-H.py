#!/usr/bin/env python
# coding: utf-8

from pathlib import Path
import numpy as np
import json
from astropy.io import fits
from astropy.utils.misc import JsonCustomEncoder
import astropy.units as u
from matplotlib import pyplot as plt
import seaborn as sns
import sys
import turbustat.statistics as tss
from turbustat.statistics import PowerSpectrum
from turbustat.io.sim_tools import create_fits_hdu





datapath_obs= Path(open("path-observations.txt", "r").read()).expanduser()
datapath_data = Path(open("path-results.txt", "r").read()).expanduser()


name = 'TAU-N604-H'
name_file = 'TAURUS-604-Ha-RV-mod.fits'
distance = 840000 #parsecs
pix = 0.26 #arcsec 


data = json.load(open(str(datapath_data) + '/' + name + ".json"))
rad_vel =fits.open(datapath_obs / name_file)


rad_vel.info()


hdr = rad_vel[0].header


hdr ['CDELT1'] = (-pix / (60*60), '[deg] Coordinate increment at reference point')
hdr ['CDELT2'] = (pix / (60*60), '[deg] Coordinate increment at reference point')
hdr['CUNIT1']  = ('deg' , 'Units of coordinate increment and value' )      
hdr['CUNIT2']  = ('deg' , 'Units of coordinate increment and value'  )
hdr['CTYPE1']  = ('RA---CAR', 'Right ascension, plate caree projection  ')
hdr['CTYPE2']  = ('DEC--CAR', 'Declination, plate caree projection   ')


hdr


rad_vel.info()


##nan values to mean velocity values
vmed = np.nanmedian(rad_vel[0].data)
m = np.isfinite(rad_vel[0].data)
rad_vel[0].data[~m] = vmed


vv = rad_vel[0].data.astype(float)
##load  thecorrelation length and seeing derived from the fit
r0 = data["results_2sig"]['r0'][0] #pc
s0 = data["results_2sig"]['s0'][0] #pc
r0,s0






fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot()

sns.heatmap(vv, cmap="RdBu_r",cbar_kws={'label': 'km/s'})
ax.set_facecolor('xkcd:gray')
ax.set_xlabel('X')
ax.set_ylabel('Y')


##img_hdu = create_fits_hdu(img, pixel_scale, beamfwhm, imshape, restfreq, bunit)
#img_hdu = create_fits_hdu(vv,pix*u.arcsec,1 * u.arcsec, vv.shape, 1 * u.Hz, u.K)
#img_hdu.header


#pspec = PowerSpectrum(img_hdu, distance=distance* u.pc) 


pspec = PowerSpectrum(vv, header = hdr, distance=distance* u.pc) 
#pspec.run(verbose=True, xunit=u.pc**-1)
pspec.run(verbose=True, xunit=u.pc**-1, low_cut=(r0*u.pc)**-1, high_cut=(s0*u.pc)**-1)


pspec.slope


(r0*u.pc)**-1,(s0*u.pc)**-1,0.01*(u.pc)**-1


np.log10(1/s0)*(u.pc)**-1,-1.75*(u.pc)**-1,-1.0*(u.pc)**-1


pspec = PowerSpectrum(vv, header = hdr, distance=distance * u.pc) 

pspec.run(verbose=True, xunit=(u.pc)**-1, low_cut=0.01*(u.pc)**-1, high_cut=(1/s0)*(u.pc)**-1,
          fit_kwargs={'brk': (1/r0)*(u.pc)**-1, 'log_break': False}, fit_2D=False)  


dvar = tss.DeltaVariance(vv, header = hdr, distance=distance* u.pc)


plt.figure(figsize=(14, 8))
dvar.run(verbose=True, boundary="fill",xunit=u.pc, xlow=s0*u.pc, xhigh=r0*u.pc)


#sns.set_context("talk", font_scale=1.1)
#plt.style.use(["seaborn-poster",])





fig, (ax, axx) = plt.subplots(
    1,
    2,
    sharey=False,
    figsize=(15, 4),
)

##spatial power spectra
ax.scatter(pspec.freqs,pspec.ps1D)
#ax.scatter(pspec.freqs,pspec.ps1D_stddev)
#ax.errorbar(np.array(pspec.freqs), pspec.ps1D, yerr=(pspec.ps1D_stddev/pspec.ps1D)*0.434, ls="", elinewidth=0.4, alpha=1.0, c="k")

ax.axvline(1/r0, c="b")
ax.axvline(1/s0, c="k")

#xgrid = np.linspace(1/r0,1/s0, 200)
#ax.plot(xgrid, (10**4.6)*xgrid**pspec.slope, '-', c="k")

ax.set(xscale='log', yscale='log', 
       xlabel='log spatial frequency $k$,1/pc',
       ylabel=r'log $P(k)_2,\ \mathrm{-}$'
      )

##delta-variance
axx.scatter(dvar.lags,dvar.delta_var*dvar.data.var())
axx.scatter(data['r'],data['B'])
axx.set(xscale='log', yscale='log', 
       xlabel='log lags,pc',
       ylabel=r'log $\Delta, \mathrm{-}$'
      )

axx.axvline(r0, c="b")
axx.axvline(s0, c="k")


plt.scatter(data['r'],data['B'])


get_ipython().system('jupyter nbconvert --to script --no-prompt ps-TAU-N604-H.ipynb')

