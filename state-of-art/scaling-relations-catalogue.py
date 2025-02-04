#!/usr/bin/env python
# coding: utf-8

# This is Will's edit of a notebook originally written by Javier.
# 
# # Correlations between H II region parameters
# 
# We look at correlations between 6 principal measurements that fall into two groups: 
# 
# * Basic parameters: 
#     * Size: $S$
#     * Ionizing luminosity: $L(\mathrm{H\alpha})$
#     * Distance: $d$
#     * Velocity dispersion on line of sigth: $\sigma_{\text{los}}$
# * Velocity structure function parameters:
#     * Velocity dispersion on plane of sky: $\sigma_{\text{pos}}$
#     * Velocity autocorrelation length scale: $r_0$
#     * Structure function slope in inertial range: $m$

from pathlib import Path


import time
start_time=time.time()
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import os
import lmfit
import statsmodels.api as sm
import linmix
from scipy.stats import pearsonr
import pickle
import math
import itertools
import json
from logerr import logify


# Load Table with physical properties

physical_data = pd.read_table('property-regions-data.csv', delimiter=',')
#physical_data = physical_data.drop(physical_data .index[[5,7]])


# Path names

datapath_names = Path(open("path-name-list.txt", "r").read()).expanduser()


samples=pd.read_csv(str(datapath_names) +'//sample-names-corr.csv',header=None)
Names=pd.read_csv(str(datapath_names) +'//formal-names-corr.csv',header=None)


# Load Results

datapath_res = Path(open("path-results.txt", "r").read()).expanduser()





data = {}
Results = {}

for i in range(len(samples)):
    data[samples[0][i]] = json.load(open(str(datapath_res) + '/' + samples[0][i] + ".json"))


#sigma
sig = [[0]*(1) for i in range(len(samples))]
siger = [[0]*(1) for i in range(len(samples))]

#velocity dispersion with 2-sig intervals
sig2 = [[0]*(1) for i in range(len(samples))]
#sig2er = [[0]*(1) for i in range(len(samples))]
sig2s2 = [[0]*(1) for i in range(len(samples))]
sig2s2p = [[0]*(1) for i in range(len(samples))]
sig2s2m = [[0]*(1) for i in range(len(samples))]

#correlation length with 2-sig intervals
r0 = [[0]*(1) for i in range(len(samples))]
#r0er = [[0]*(1) for i in range(len(samples))]
r0s2 = [[0]*(1) for i in range(len(samples))]
r0s2p = [[0]*(1) for i in range(len(samples))]
r0s2m = [[0]*(1) for i in range(len(samples))]

#power-law
m = [[0]*(1) for i in range(len(samples))]
#mer = [[0]*(1) for i in range(len(samples))]
ms2 = [[0]*(1) for i in range(len(samples))]
ms2p = [[0]*(1) for i in range(len(samples))]
ms2m = [[0]*(1) for i in range(len(samples))]

#noise with 2-sig intervals
bn = [[0]*(1) for i in range(len(samples))]
#ner = [[0]*(1) for i in range(len(samples))]
bns2 = [[0]*(1) for i in range(len(samples))]
bns2p = [[0]*(1) for i in range(len(samples))]
bns2m = [[0]*(1) for i in range(len(samples))]

#seeing with 2-sig intervals
s0 = [[0]*(1) for i in range(len(samples))]
#s0er = [[0]*(1) for i in range(len(samples))]
s0s2 = [[0]*(1) for i in range(len(samples))]
s0s2p = [[0]*(1) for i in range(len(samples))]
s0s2m = [[0]*(1) for i in range(len(samples))]

pc = [[0]*(1) for i in range(len(samples))]
box_size = [[0]*(1) for i in range(len(samples))]


for i in range(len(samples)):    
    
    sig2[i] = data[samples[0][i]]['results_2sig']['sig2'][0]
    sig2s2p[i] = data[samples[0][i]]['results_2sig']['sig2'][1]
    sig2s2m[i] = data[samples[0][i]]['results_2sig']['sig2'][2]
    
    r0[i]    = data[samples[0][i]]['results_2sig']['r0'][0]
    r0s2p[i] = data[samples[0][i]]['results_2sig']['r0'][1]
    r0s2m[i] = data[samples[0][i]]['results_2sig']['r0'][2]
    
    m[i]    = data[samples[0][i]]['results_2sig']['m'][0]
    ms2p[i] = data[samples[0][i]]['results_2sig']['m'][1]
    ms2m[i] = data[samples[0][i]]['results_2sig']['m'][2]
    
    bn[i]    = data[samples[0][i]]['results_2sig']['noise'][0]
    bns2p[i] = data[samples[0][i]]['results_2sig']['noise'][1]
    bns2m[i] = data[samples[0][i]]['results_2sig']['noise'][2]
    
    s0[i]    = data[samples[0][i]]['results_2sig']['s0'][0]
    s0s2p[i] = data[samples[0][i]]['results_2sig']['s0'][1]
    s0s2m[i] = data[samples[0][i]]['results_2sig']['s0'][2]
    
    box_size[i] = data[samples[0][i]]['properties']['box_size']
    pc[i] = data[samples[0][i]]['properties']['pc']


s0f = pd.DataFrame(
    {
        "s0 [RMS]":s0,
        "s0+[RMS]": s0s2p,
        "s0-[RMS]": s0s2m,  
       "s0 [FWHM]": np.array(s0)*2.35/np.array(pc),
       "s0- [FWHM]": np.array(s0s2m)*2.35/np.array(pc),
       "s0+ [FWHM]": np.array(s0s2p)*2.35/np.array(pc),
        "bn ":bn,
        "bn+": bns2p,
        "bn- ": bns2m,     
    }
)

s0f.insert(loc=0, column='Region', value=Names)


s0f.round(4)


s1f = pd.DataFrame(
    {
        "sig2":sig2,
        "sig2+": sig2s2p,
        "sig2-": sig2s2m,
        "r0":r0,
        "r0+": r0s2p,
        "r0-": r0s2m,
        "m":m,
        "m+": ms2p,
        "m-": ms2m,
       
    }
)

s1f.insert(loc=0, column='Region', value=Names)


s1f.round(4)


physical_data


data = pd.DataFrame(
    {
       "Region": physical_data.Region,
       "LHa": physical_data.LHa,
       "LHaer": physical_data.LHaer,
       "SFR": physical_data.SFR,
       "n": physical_data.n,
       "L [pc]": physical_data['Diam [pc]'],
       "Ler [pc]": physical_data['Diamer [pc]'],
       "Dist [kpc]": physical_data['Dist [kpc]'],
       "Dister [kpc]": physical_data['Dister [kpc]'],
        
       "sig2 [km/s]": sig2,
       "sig2er": sig2s2p,
        "sig [km/s]": np.array(sig2)**0.5,
       "siger": np.array(sig2s2p)**0.5,
        "m": m,
       "mer": ms2p,
       "r0 [pc]": r0,
       "r0er": r0s2p,
        
       "siglos [km/s]": physical_data['siglos [km/s]'],
       "sigloser [km/s]": physical_data['sigloser [km/s]'],
      
    },
)


data.dtypes


data.round(4)


cols = data.columns
logdata = data.copy()
for col in cols:
    if col not in ["Region", "m", "mer", "r0er", "siger",  "sig2er", "Ler [pc]", "Dister [kpc]","LHaer","sigloser [km/s]"]:
        logdata[col] = np.round(np.log10(logdata[col]), 2)
        logdata.rename(columns={col: f"log {col}"}, inplace=True)
# Some minor changes to column names
logdata.rename(
    columns={
        "log LHa": "log L(H) [erg s^-1]",
        }, 
    inplace=True)
logdata


# Uncertainties Log Space

logdata['Ler [pc]']=(data['Ler [pc]']/data['L [pc]'])*0.434
logdata['sigloser [km/s]']=(data['sigloser [km/s]']/data['siglos [km/s]'])*0.434
logdata['LHaer']=(data['LHaer']/data['LHa'])*0.434
logdata['Dister [kpc]']=(data['Dister [kpc]']/data['Dist [kpc]'])*0.434
logdata['mer']=(data['mer']/data['m'])*0.434
logdata['r0er']=(data['r0er']/data['r0 [pc]'])*0.434
logdata['siger']=(data['siger']/data['sig [km/s]'])*0.434
logdata['sig2er']=(data['sig2er']/data['sig2 [km/s]'])*0.434


#logify(data['L [pc]'],data['Ler [pc]'])


# Make the label text bigger on the figures

sns.set_context("talk")


selected_vars = [ "log L [pc]","log L(H) [erg s^-1]", "log Dist [kpc]", "m", "log r0 [pc]", "log sig [km/s]", "log siglos [km/s]"]
plotdata = logdata[selected_vars].rename(
    columns={
        # Switch column names to use latex formatting to improve axis labels
        "log L [pc]": r"$\log_{10}\ L$ [pc]", 
        "log L(H) [erg s^-1]": r"$\log_{10}\ L(\mathrm{H})$ [erg s$^{-1}$]", 
        "m": "$m$", 
        "log r0 [pc]": r"$\log_{10}\ r_0$ [pc]", 
        "log sig [km/s]": r"$\log_{10}\ \sigma$ [km/s]", 
        "log Dist [kpc]": r"$\log_{10}\ D$ [kpc]",
    },
)

sns.pairplot(plotdata, 
             hue=r"$\log_{10}\ D$ [kpc]",
             plot_kws=dict(alpha=0.75, s=200, edgecolor="k"), 
             diag_kind='hist',
             diag_kws= dict(multiple='stack'),
             );

figname = "strucfunc-correlations"
# Save PDF and JPG versions of the figure
#plt.gcf().savefig(f"{figname}.pdf")
#plt.gcf().savefig(f"{figname}.jpg")


# ## Comparion previous work
# 
# 

# ## L vs Sig

sns.set_context("talk", font_scale=1.2)


path_previous = 'data-previous-scaling-relations'


Ostin = pd.read_csv(path_previous+'//Ostin2001.csv')
Blasco = pd.read_csv(path_previous+'//Blasco2013.csv')
Rozas = pd.read_csv(path_previous+'//Rozas2006.csv')
Ars = pd.read_csv(path_previous+'//ArsRoy1986.csv')
Wis = pd.read_csv(path_previous+'//Wis2012.csv')
Gal = pd.read_csv(path_previous+'//Gallagher1983.csv')
Fer = pd.read_csv(path_previous+'//Fernandez2018.csv')
TM81 = pd.read_csv(path_previous + '//TM1981.csv')
Ch14 = pd.read_csv(path_previous + '//Chavez2014.csv')
Moiseev = pd.read_csv(path_previous+'//Moiseev2015.csv')

MoiLV = pd.read_csv(path_previous+'//MoiLV2015.csv')
MoiXMD = pd.read_csv(path_previous+'//MoiXMD2015.csv')
MoiBCDG = pd.read_csv(path_previous+'//MoiBCDG2015.csv')


logdata['log siglos [km/s]']


fig, ax=plt.subplots(figsize=(10,10))

#plt.scatter(Fer.L,10**(Fer.sig),label='Fernandez 2018',marker='.',alpha=0.95,color='darkgray')
#plt.scatter(logdata['log L(H) [erg s^-1]'],10**(logdata['log siglos [km/s]']),marker='v',label='SigLOS',color='black',s=(logdata['log Dist [kpc]']+1.0)*70)

#HB
plt.scatter(Ch14.sig,Ch14.L,label='Galaxias HII',marker='.',alpha=0.95,color='blue')
plt.scatter(np.log10(TM81.sig),TM81.L,label='GEHRs',marker='.',alpha=0.95,color='red')
#Ha
plt.scatter(np.log10(MoiLV.sig),MoiLV.L-0.45,label='Galaxias enanas',marker='.',alpha=0.75,color='orange')
plt.scatter(np.log10(MoiXMD.sig),MoiXMD.L-0.45,label='Galaxias XMD' ,marker='X',alpha=0.75,color='orange')
plt.scatter(np.log10(MoiBCDG.sig),MoiBCDG.L-0.45,label='BCDG',marker='^',alpha=0.75,color='orange')
plt.scatter(np.log10(Wis.sig),Wis.L-0.45,label='clumps',marker='o',alpha=0.75,color='lime')
plt.scatter(logdata['log sig [km/s]'],logdata['log L(H) [erg s^-1]']-0.45,marker='o',label='$σ_{pos}$',color='black')
plt.scatter(logdata['log siglos [km/s]'],logdata['log L(H) [erg s^-1]']-0.45,marker='x',label='$σ_{los}$',color='black')
#plt.scatter(Rozas.sig,Rozas.L-0.45,label='Rozas 2006',marker='.',alpha=0.95,color='darkgray')


ax.set(
#    ylim  = [36, 43],
#    xlim  = [1, 150],
)
#ax.set_facecolor('whitesmoke')
#plt.yscale('log')

ax.set(ylabel='Log(L$_{Hβ}$) [erg/s]', xlabel='Log $σ$ [km s$^{-1}$]')
plt.legend()
fig.savefig('plots//l_vs_s_global.pdf', bbox_inches='tight')


global_sig = pd.concat([Ch14.sig,np.log10(TM81.sig),np.log10(MoiLV.sig),np.log10(MoiXMD.sig),np.log10(MoiBCDG.sig),np.log10(Wis.sig),logdata['log sig [km/s]']], axis = 0)
global_L = pd.concat([Ch14.L,TM81.L,MoiLV.L-0.45,MoiXMD.L-0.45,MoiBCDG.L-0.45,Wis.L-0.45,logdata['log L(H) [erg s^-1]']-0.45], axis = 0)


global_sig_er = (global_sig *.05)/global_sig 
global_L_er = (global_L *.05)/global_L 


X, Xe, Y, Ye = [global_sig, global_sig_er, global_L, global_L_er]
lm = linmix.LinMix(X, Y, Xe, Ye, K=2)
lm.run_mcmc()


dfchain = pd.DataFrame.from_records(
    lm.chain.tolist(), 
    columns=lm.chain.dtype.names
)
#dfchain


pearsonr(X, Y)


pd.DataFrame({"X": X, "Xe": Xe, "Y": Y, "Ye": Ye}).describe()


vmin, vmax = 0.25, 2.5
xgrid = np.linspace(vmin, vmax, 200)


fig, ax = plt.subplots(figsize=(10, 10))

ax.errorbar(X, Y, xerr=Xe, yerr=Ye, ls=" ", elinewidth=0.4, alpha=1.0, c="k")
ax.scatter(X, Y, marker=".", s=20/np.hypot(Xe, Ye))
# The original fit
ax.plot(xgrid, dfchain["alpha"].mean() + xgrid*dfchain["beta"].mean(), 
        '-', c="k")


for samp in lm.chain[::100]:
    ax.plot(xgrid, samp["alpha"] + xgrid*samp["beta"], 
        '-', c="r", alpha=0.15, lw=0.35,zorder=0)
    
ax.text(.05, .95,'log  (L$_{Hβ}$)= (' 
        + str(np.round(dfchain["beta"].mean(),3)) + '$\pm$' + str(np.round(dfchain["beta"].std(),3))
        + ')log $\sigma$+('
        + str(np.round(dfchain["alpha"].mean(),3)) + '$\pm$' + str(np.round(dfchain["alpha"].std(),3))
        + ')',  color='k', transform=ax.transAxes)
    
ax.set(xlim=[0.25, 2.5], ylim=[36, 44],ylabel='Log(L$_{Hβ}$) [erg/s]', xlabel='Log $σ$ [km s$^{-1}$]')
fig.savefig('plots//global_L_s.pdf', bbox_inches='tight')


# ## D vs Sig

MelDS = pd.read_csv(path_previous+'//MelDS1977.csv')
LarDS = pd.read_csv(path_previous+'//LarDS1981.csv')
TMDS = pd.read_csv(path_previous+'//TMDS1981.csv')
TMDSEG = pd.read_csv(path_previous+'//TMDS1981EG.csv')
ARDSA = pd.read_csv(path_previous+'//ARDS1988.csv')
WDS = pd.read_csv(path_previous+'//WisDS2012.csv')


fig, ax=plt.subplots(figsize=(10,10))

plt.scatter(MelDS.sig,MelDS.D,label='GEHRs',marker='.',alpha=0.95,color='blue')
plt.scatter(LarDS.sig,LarDS.D,label='MCs',marker='.',alpha=0.95,color='red')
plt.scatter(TMDS.sig,TMDS.D,label='GEHRs',marker='s',alpha=0.95,color='orange')
plt.scatter(TMDSEG.sig,TMDSEG.D,label='EG',marker='.',alpha=0.95,color='orange')
plt.scatter(ARDSA.sig,ARDSA.D,label='GEHRs',marker='.',alpha=0.95,color='green')
plt.scatter(np.log10(WDS.sig),np.log10(WDS.D),label='clumps',marker='.',alpha=0.95,color='lime')

plt.scatter(logdata['log sig [km/s]'],logdata['log L [pc]'],marker='o',label='$σ_{pos}$',color='black')
plt.scatter(logdata['log siglos [km/s]'],logdata['log L [pc]'],marker='x',label='$σ_{los}$',color='black')


ax.set(
#    ylim  = [36, 43],
#    xlim  = [1, 150],
)
#ax.set_facecolor('whitesmoke')
#plt.yscale('log')

ax.set(ylabel='Log D [pc]', xlabel='Log $σ$ [km s$^{-1}$]')
plt.legend()
fig.savefig('plots//d_vs_s_global.pdf', bbox_inches='tight')





global_sig = pd.concat([MelDS.sig,LarDS.sig,TMDS.sig,TMDSEG.sig,ARDSA.sig,np.log10(WDS.sig),logdata['log sig [km/s]']], axis = 0)
global_D = pd.concat([MelDS.D,LarDS.D,TMDS.D,TMDSEG.D,ARDSA.D,np.log10(WDS.D),logdata['log L [pc]']], axis = 0)


global_sig_er = (global_sig *.05)/global_sig 
global_D_er = (global_D *.05)/global_D 


X, Xe, Y, Ye = [global_sig, global_sig_er, global_D, global_D_er]
lm = linmix.LinMix(X, Y, Xe, Ye, K=2)
lm.run_mcmc()


dfchain = pd.DataFrame.from_records(
    lm.chain.tolist(), 
    columns=lm.chain.dtype.names
)
#dfchain


pearsonr(X, Y)


pd.DataFrame({"X": X, "Xe": Xe, "Y": Y, "Ye": Ye}).describe()


vmin, vmax = -0.5, 3.0
xgrid = np.linspace(vmin, vmax, 200)


fig, ax = plt.subplots(figsize=(10, 10))

ax.errorbar(X, Y, xerr=Xe, yerr=Ye, ls=" ", elinewidth=0.4, alpha=1.0, c="k")
ax.scatter(X, Y, marker=".", s=20/np.hypot(Xe, Ye))
# The original fit
ax.plot(xgrid, dfchain["alpha"].mean() + xgrid*dfchain["beta"].mean(), 
        '-', c="k")


for samp in lm.chain[::100]:
    ax.plot(xgrid, samp["alpha"] + xgrid*samp["beta"], 
        '-', c="r", alpha=0.15, lw=0.35,zorder=0)
    
ax.text(.05, .95,'log  D= (' 
        + str(np.round(dfchain["beta"].mean(),3)) + '$\pm$' + str(np.round(dfchain["beta"].std(),3))
        + ')log $\sigma$+('
        + str(np.round(dfchain["alpha"].mean(),3)) + '$\pm$' + str(np.round(dfchain["alpha"].std(),3))
        + ')',  color='k', transform=ax.transAxes)
    
ax.set(ylabel='Log D [pc]', xlabel='Log $σ$ [km s$^{-1}$]')
fig.savefig('plots//global_d_s.pdf', bbox_inches='tight')


# ## other stuff



fig, ax=plt.subplots(figsize=(9,9))

plt.scatter(Gal.L,Gal.sig,label='Gallagher 1983',marker='x',alpha=0.85,color='dimgray')
plt.scatter(Ars.L,10**Ars.sig,label='Arsenault 1988',marker='+',alpha=0.85,color='dimgray')
plt.scatter(Ostin.L,Ostin.sig,label='Ostin 2001',marker='o',alpha=0.95,color='darkgray')
plt.scatter(Rozas.L,10**(Rozas.sig),label='Rozas 2006',marker='.',alpha=0.95,color='darkgray')
plt.scatter(Wis.L,Wis.sig,label='Wisnioski 2012',marker='s',alpha=0.75,color='silver')
plt.scatter(Blasco.L,Blasco.sig,label='Blasco 2013',marker='D',alpha=0.75,color='silver')
plt.scatter(Moiseev.L,Moiseev.sig,label='Moiseev 2015',marker='^',alpha=0.75,color='silver')

plt.scatter(logdata['log L(H) [erg s^-1]'],10**(logdata['log sig [km/s]']),marker='o',label='SigPOS',color='black',s=(logdata['log Dist [kpc]']+1.0)*70)
plt.scatter(logdata['log L(H) [erg s^-1]'],10**(logdata['log siglos [km/s]']),marker='v',label='SigLOS',color='black',s=(logdata['log Dist [kpc]']+1.0)*70)

plt.yscale('log')

ax.set(
#    ylim  = [36, 43],
#    xlim  = [1, 150],
)
#ax.set_facecolor('whitesmoke')
ax.set(xlabel='Log(L$_{Hα}$) [erg/s]', ylabel='$σ$ [km s$^{-1}$]')
plt.legend()







globalL= pd.concat([Moiseev.L, Ostin.L.dropna(),Blasco.L.dropna(),Rozas.L.dropna(),Ars.L.dropna(),Wis.L.dropna(),Gal.L.dropna()], axis=0)
globalS= pd.concat([Moiseev.sig, Ostin.sig.dropna(),Blasco.sig.dropna(),10**Rozas.sig.dropna(),10**Ars.sig.dropna(),Wis.sig.dropna(),Gal.sig.dropna()],  axis=0)
GL=np.concatenate((np.array(globalL), np.array(logdata['log L(H) [erg s^-1]'])))
GS=np.concatenate((np.array(globalS), np.array(10**(logdata['log siglos [km/s]']))))


GSer = (GS*.05)/GS


GLer = (GL*.05)/GL


X, Xe, Y, Ye = [GL, GLer, np.log10(GS), GSer]
lm = linmix.LinMix(X, Y, Xe, Ye, K=2)
lm.run_mcmc()




dfchain = pd.DataFrame.from_records(
    lm.chain.tolist(), 
    columns=lm.chain.dtype.names
)
#dfchain


pearsonr(X, Y)


a = pearsonr(X, Y)


pd.DataFrame({"X": X, "Xe": Xe, "Y": Y, "Ye": Ye}).describe()


vmin, vmax = 36, 44
xgrid = np.linspace(vmin, vmax, 200)


fig, ax = plt.subplots(figsize=(10, 10))

ax.errorbar(X, Y, xerr=Xe, yerr=Ye, ls=" ", elinewidth=0.4, alpha=1.0, c="k")
ax.scatter(X, Y, marker=".", s=20/np.hypot(Xe, Ye))
# The original fit
ax.plot(xgrid, dfchain["alpha"].mean() + xgrid*dfchain["beta"].mean(), 
        '-', c="k")
for samp in lm.chain[::20]:
    ax.plot(xgrid, samp["alpha"] + xgrid*samp["beta"], 
        '-', c="r", alpha=0.2, lw=0.1)
    
ax.text(.05, .95,'log $\sigma$ = (' 
        + str(np.round(dfchain["beta"].mean(),3)) + '$\pm$' + str(np.round(dfchain["beta"].std(),3))
        + ')log L(H)+('
        + str(np.round(dfchain["alpha"].mean(),3)) + '$\pm$' + str(np.round(dfchain["alpha"].std(),3))
        + ')',  color='k', transform=ax.transAxes)
    
ax.set(
#    xlim=[-0.2, 0.8], ylim=[-0.2, 0.8],
    xlabel=r"log L(H) [erg s^-1]", ylabel=r"log $\sigma$ [km/s]",
)








print("--- %s seconds ---" % (time.time()-start_time))


get_ipython().system('jupyter nbconvert --to script --no-prompt scaling-relations-catalogue.ipynb')

