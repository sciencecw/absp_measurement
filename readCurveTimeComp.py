import numpy as np
import matplotlib.pyplot as pyt

## take all curves of the same sample (particular material and batch) 
## and compare the spectrum

## Also usable as a replacement to readCurveRefCheck.py, 
## to compare with past refs

from datetime import date
import sys
from Curve import (Curve, curvesKeyword, curveCreation, 
					specPlotter,curvesAge, curvesRef, readCurveFile)


execfile('readCurveInput_default.py') # loads default setting
execfile('readCurveInput_0708test.py')


allc = curvesKeyword(allcurves, name = keyword) 
allc2 = curvesKeyword(allcurves, name = keyword2)
refc = curvesKeyword(refcurves, name = refkeyword) 
cref = refc[refnum]

fig, (ax1,ax2) = pyt.subplots(2,1, sharex=True, gridspec_kw=shr, figsize = figsize)


if baseline:
	t , df = False, False
	tLabel = 'Transmission'
fig.suptitle(eval(titleGen), y=.95, size=17)
iterfarb, iterfarb2 =  iter(farben),iter(farben2)
numPlotted = 0
if showRef:
	lbl = cref.nametag #str(c.datetag)
	ax1.plot(x[s],cref.avgcurve(t=t)[s], label = 'Ref ' + lbl,
			 color = 'blue',linewidth = 1.5)

if isFirstLast:
	# Only first and last sample to show agregate change
	for array in [allc,allc2]:
		c = array[0]
		clr = iterfarb2.next()
		lbl = c.label() if isOrigLabel else cLabel[numPlotted]
		ax1.plot(x[s],c.avgcurve(t=t)[s], label = lbl, color = clr, 
					linestyle = 'dashed',linewidth = 1.7)
		numPlotted+=1
	for array in [allc,allc2]:
		c = array[-1]
		clr = iterfarb.next()
		lbl = c.label() if isOrigLabel else cLabel[numPlotted]
		ax1.plot(x[s],c.avgcurve(t=t)[s], label = lbl, color = clr,linewidth = 1.2)
		numPlotted+=1
else:
	for c in allc:
		clr = iterfarb.next()
		lbl = c.label() if isOrigLabel else cLabel[numPlotted]
		ax1.plot(x[s],c.avgcurve(t=t)[s], label = lbl, color = clr,linewidth = 1)
		numPlotted+=1
	for c in allc2:
		clr = iterfarb2.next()
		lbl = c.label() if isOrigLabel else cLabel[numPlotted]
		ax1.plot(x[s],c.avgcurve(t=t)[s], label = lbl, color = clr,linewidth = 1)#, linestyle = 'dashed')
		numPlotted+=1

if not baseline and showErr:
	ax1.plot(x[s],allc[0].errcurve(t=t)[s]*10, label = 'Error x10', color = 'cyan')
ax1.grid(True)
ax1.legend(loc = 0, fontsize = legFont)
ax1.set_xlabel('Wavelength nm')
ax1.set_ylabel(tLabel)
if t:
	ax1.set_ylim([0.,1.])

avgpcterr = np.abs(cref.errcurve(t=t))/cref.avgcurve(t=t)
# to show diff in absp plots
if (not t) and df:
	avgpcterr = np.abs(cref.errcurve(t=t))
if not baseline:
	# error shades
	ax2.fill_between(x[s],-avgpcterr[s],avgpcterr[s], label = 'err',alpha = .3) #default .2
iterfarb, iterfarb2 =  iter(farben), iter(farben2)
if isFirstLast:
	# Only first and last sample to show agregate change
	ref = cref.avgcurve(t=t)
	for array in [allc,allc2]:
		c = array[0]
		avg = c.avgcurve(t=t)
		ax2.plot(x[s],(avg/ref-1)[s],
		  	  linestyle='dashed', linewidth = 1.8, color = iterfarb2.next())
	for array in [allc,allc2]:
		c = array[-1]
		avg = c.avgcurve(t=t)
		ax2.plot(x[s],(avg/ref-1)[s],
				linewidth = 1.2, color = iterfarb.next())
else:
	for c in allc:
		if (not t) and df:
			ax2.plot(x[s],(c.avgcurve(t=t)-cref.avgcurve(t=t))[s],   color = iterfarb.next())
		else: 
			ax2.plot(x[s],(c.avgcurve(t=t)/cref.avgcurve(t=t)-1)[s], 
				linewidth = 1.5, color = iterfarb.next())
	for c in allc2:
		if (not t) and df:
			ax2.plot(x[s],(c.avgcurve(t=t)-cref.avgcurve(t=t))[s], 
				color = iterfarb2.next())#, linestyle = 'dashed')
		else: 
			ax2.plot(x[s],(c.avgcurve(t=t)/cref.avgcurve(t=t)-1)[s], 
				color = iterfarb2.next())#, linestyle = 'dashed')

ax2.grid(True)
ax2.set_xlabel('Wavelength nm')
ax2.set_ylabel('Diff' if (not t) and df else 'Ratio-1')
ax2.set_ylim(ratioyrange)
pyt.show(block = isBlocked)
#fig.savefig('plots/SpecCompPS-PVT-6_7/SpecComp'+refkeyword+'.png')
