## take all curves of the same sample (particular material and batch) 
## and compare the spectrum

## Also usable as a replacement to readCurveRefCheck.py, 
## to compare with past refs

## version new: rearranged and merged the curve and ratio plotting procedures





# july 9th: check readCurveSequence for similar capability

import numpy as np
import matplotlib.pyplot as pyt
from datetime import date
import sys
from Curve import (Curve, curvesKeyword, curveCreation, keycGen,
					specPlotter,curvesAge, curvesRef, readCurveFile)


execfile('readCurveInput_default.py') # loads default setting
execfile('readCurveInput_260PVTDiff.py')
allc = curvesKeyword(allcurves, name = keyword) 
allc2 = curvesKeyword(allcurves, name = keyword2)
refc = curvesKeyword(refcurves, name = refkeyword) 
cref = refc[refnum]

fig, (ax1, ax2) = pyt.subplots(2,1, sharex=True, gridspec_kw=shr,figsize = (8,8))


## TITLES and labels
fig.suptitle(eval(titleGen), y=.95, size=17)
iterfarb, iterfarb2 =  iter(farben),iter(farben2)


# DRAW REFERENCE AND ERROR 
if showRef:
	lbl = cref.nametag #str(c.datetag)
	ax1.plot(x[s],cref.avgcurve(t=t)[s], label = 'Ref ' + lbl,
			 color = iterfarb.next(),linewidth = 1.5)
avgpcterr = np.abs(cref.errcurve(t=t))/cref.avgcurve(t=t)
if (not t) and df: 
	# to show diff in absp plots
	avgpcterr = np.abs(cref.errcurve(t=t))

# error curves
ax1.plot(x[s],allc[0].errcurve(t=t)[s]*10, label = 'Error x10', color = 'cyan')
ax2.fill_between(x[s],-avgpcterr[s],avgpcterr[s], label = 'err',alpha = .3) #default .2


ref = cref.avgcurve(t=t)[s]

for c in allc:
	Curve.compPlotter(ax1,ax2,x[s], c.avgcurve(t=t)[s], ref, 1., 1.,
						color = iterfarb.next(), label = c.label())	
for c in allc2:
	Curve.compPlotter(ax1,ax2,x[s], c.avgcurve(t=t)[s], ref, 1.3, 1.,
					color = iterfarb2.next(), label = c.label())

ax1.grid(True)
ax1.legend(loc = 0, fontsize = legFont)
ax1.set_xlabel('Wavelength nm')
ax1.set_ylabel(tLabel)
if t:
	ax1.set_ylim([0.,1.])
ax2.grid(True)
ax2.set_xlabel('Wavelength nm')
ax2.set_ylabel('Diff' if (not t) and df else 'Ratio-1')
ax2.set_ylim(ratioyrange)
pyt.show(block = isBlocked)
#fig.savefig('plots/SpecCompPS-PVT-6_7/SpecComp'+refkeyword+'.png')






