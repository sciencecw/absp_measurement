## take 2 samples (particular material and batch) 
## and compare the spectrum of each of the 4 sides
## adapted from readCurveTimeComp_new
##
##   Created: Oct 13


import numpy as np
import matplotlib.pyplot as pyt
from datetime import date
import sys
from Curve import (Curve, curvesKeyword, curveCreation, keycGen,
					specPlotter,curvesAge, curvesRef, readCurveFile, getAllCsv)
from Curve_TimeFit import Curve_TimeFit

execfile('readCurveInput_default.py') # loads default setting
def datemake(string):
	ymd = (string[8:12],string[12:14],string[14:16])
	return date(*map(int,ymd))

fnList = getAllCsv()
allctemp = []
for n in fnList:
	try:
		allctemp += curveCreation(datemake(n),[n,],verbose=1, skips=2)
	except ValueError:
		print 'Date cannot be obtained:', n

keyword = sys.argv[1] #'EJ200SP-1P-N1'
allcurves = curvesKeyword(allctemp, name = keyword)
#print [c.len() for c in allcurves]
 
s =  Curve.makeslice(300,600)
ratioyrange= [-0.05,0.05]

xarray = []#[0,[],[],[],[]]
#try:
for c in allcurves:
	xc = Curve_TimeFit.steplocTrsmQuadMem2(c)[0]
	xarray.append(xc)
#except:#
#	pass

xarray = zip(*xarray)
xarray = [[v for v in vector if v > 0] for vector in xarray]
xbigArray = np.array(sum(xarray,[]))
medx, avgx, sdx = np.median(xbigArray), np.average(xbigArray), np.std(xbigArray)
print 'median: ', medx
print 'average: ', avgx
print 'SD: ',  sdx
rge = (medx - .7, medx + .7) if np.ptp(xbigArray) > 2 * sdx else None

fig, (ax1, ax2) = pyt.subplots(1,2, figsize = (8,5), sharex=True)
ax1.hist(xarray,bins = 15   , histtype='step', range = rge)
ax2.hist(xbigArray,bins = 40, histtype='step', range = rge)
ax1.set_xlabel('wavelength')
ax2.set_xlabel('wavelength')
ax1.set_ylabel('counts')
fig.suptitle(keyword + ' Step Distribution', y=.97, size = 15)
pyt.show(block = False)

if False:
	fig, (ax1, ax2) = pyt.subplots(2,1, sharex=True, gridspec_kw=shr,figsize = (8,8))
	## TITLES and labels
	fig.suptitle(eval(titleGen), y=.95, size=17)


	ax1.legend(loc = 0, fontsize = legFont)
	if t:
		ax1.set_ylim([0.,1.])
	ax2.set_ylim(ratioyrange)
	pyt.show(block = isBlocked)
	#fig.savefig('plots/SpecCompPS-PVT-6_7/SpecComp'+refkeyword+'.png')
