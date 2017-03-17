## take all curves of the same sample (particular material and batch) 
## and compare the spectrum

## Also usable as a replacement to readCurveRefCheck.py, 
## to compare with past refs

## version new: rearranged and merged the curve and ratio plotting procedures

import numpy as np
import matplotlib.pyplot as pyt
from datetime import date
import sys
from Curve import (Curve, curvesKeyword, curveCreation, keycGen,
					specPlotter,curvesAge, curvesDate, curvesRef, readCurveFile)
import Curve_TimeFit
ctf = Curve_TimeFit.Curve_TimeFit


execfile('readCurveInput_default.py') # loads default setting
#execfile('readCurveInput_Oct_Normal.py')
#execfile('readCurveInput_Nov_varied_thickness.py')
#execfile('readCurveInput_Nov16Calib.py')	
execfile('readCurveInput_Mar17test.py')

#execfile('readCurveInput_Oct_consistency.py')	# for checking new operators consistency
#execfile('readCurveInput_July_consistency.py') # test consistency of doubly measured curves 
#execfile('readCurveInput_coldwarm_comp.py')
#execfile('readCurveInput_Normal.py')


allc = curvesKeyword(allcurves, name = keyword) 
allc2 = curvesKeyword(allcurves, name = keyword2)
refc = curvesKeyword(refcurves, name = refkeyword) 
cref = refc[refnum]
fig, (ax1, ax2) = pyt.subplots(2,1, sharex=True, gridspec_kw=shr,figsize = (8,8))

#curvesDate(allc,(2016,10,12))[0].shift(-0.3909)

## TITLES and labels
if baseline: t , df, tLabel = False, False, 'Transmission'
fig.suptitle(eval(titleGen), y=.95, size=17)
if isFarben:
	iterfarb, iterfarb2 =  iter(farben), iter(farben2)
else:
	iterfarb2 = iterfarb = Curve.NoneIter()
itercLabel = None if isOrigLabel else iter(cLabel)
iterlstyle = None if isOrigLinestyle else iter(cLineStyle)
yexp = "(avg-ref)/(avg+ref)" if isDiff else ("(avg-ref)" if ((not t) and df) else None)


# DRAW REFERENCE AND ERROR 
if showRef:
	ls = 'solid' if isOrigLinestyle else iterlstyle.next()
	lbl = 'Reference ' + cref.nametag if isOrigLabel else itercLabel.next()
	ax1.plot(x[s],avg_gen(cref), label = lbl,
			 color = iterfarb.next(),linewidth = 1.8, linestyle = ls)
avgpcterr = np.abs(cref.errcurve(t=t))/cref.avgcurve(t=t)
#avgpcterr = np.abs(allc[0].errcurve(t=t))/ allc[0].avgcurve(t=t)
if (not t) and df: 
	# to show diff in absp plots
	#avgpcterr = np.abs(sum([c.errcurve(t=t) for c in allc]))/len(allc)
	avgpcterr = np.abs(c.errcurve(t=t))
if showErr and not baseline:
	# error curves
	ax1.plot(x[s],allc[0].errcurve(t=t)[s]*10, label = 'side variation x10', color = 'cyan')
	ax2.fill_between(x[s],-avgpcterr[s],avgpcterr[s], label = 'err', alpha = .3) #default .2
	

ref = avg_gen(cref)
if isFirstLast:
	arrayallc = [ar for ar in [allc,allc2] if len(ar)>0] # check if array is empty
	for array in arrayallc:
		c = array[0]
		ls = 'dashed' if isOrigLinestyle else iterlstyle.next()
		Curve.compPlotter(ax1,ax2,x[s], avg_gen(c), ref, 1.7,1.7, yexp,
						 color = iterfarb2.next(), label = lbl_gen(c), linestyle = ls)
	for array in arrayallc:
		c = array[-1]
		ls = 'solid' if isOrigLinestyle else iterlstyle.next()
		Curve.compPlotter(ax1,ax2,x[s], avg_gen(c), ref, 1.7, 1.7, yexp,
							color = iterfarb.next(), label = lbl_gen(c), linestyle = ls)
else:
	for c in allc:
		ls = 'solid' if isOrigLinestyle else iterlstyle.next()
		Curve.compPlotter(ax1,ax2,x[s], avg_gen(c), ref, lwidth, lwidth, yexp,
							color = iterfarb.next(), label = lbl_gen(c), linestyle = ls)	
	for c in allc2:
		ls = 'solid' if isOrigLinestyle else iterlstyle.next()
		Curve.compPlotter(ax1,ax2,x[s], avg_gen(c), ref, lwidth, lwidth, yexp,
						color = iterfarb2.next(), label = lbl_gen(c), linestyle = ls)

ax1.grid(True)
ax1.legend(**leg_kwarg) #loc = legloc, fontsize = legFont)
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
