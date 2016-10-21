import numpy as np
import matplotlib.pyplot as pyt
from datetime import date

## take all curves of the same sample (particular material and batch) 
## and compare the spectrum

## Also usable as a replacement to readCurveRefCheck.py, 
## to compare with past refs

## use readCurveTimeComp if two different line style are needed

## 30 March 2016

from Curve import (Curve, curvesKeyword, curveCreation, 
					specPlotter,curvesAge, curvesRef, readCurveFile)

x= np.linspace(600,200,401)


#refcurves = readCurveFile('measuredates.txt', verbose = 0)
#allcurves = readCurveFile('measuredates_new_ref.txt', skips = 1)
allcurves = readCurveFile('measuredates_June.txt', skips = 1)
refcurves = allcurves
#allcurves = curveCreation(date(2016,04,04), ['data/EJ_20160404_air_SPN4.csv'], verbose = 1)


farben = ['blue', 'green','olive' , 'darkcyan','red','magenta','blueviolet', 'slategray','magenta']
farben += ['hotpink', 'salmon','springgreen','chocolate', 'crimson']

## parameters 
keyword = '260 1X1P N1'					# read sample
keyword2 = 'None'						# read sample
refkeyword = '260 1X1P'			# reference sample
s = slice(None)#Curve.makeslice(300,600) # x-range (band of wavelength in nm)
t = None					# transmission or absorption curve; None for absorption
df = True					# difference instead of ratio plot (for absorption curve)
showRef = True
refnum = 2 					# number of reference (from 0)
shr = dict(height_ratios = [3,2])		#subplot height ratio
newdate = True


dateN2 = date(2015,12,19)
dateN3 = date(2016,01,14)
dateN4 = date(2016,01,11)
if newdate:
	dateN4 = date(2016,03,25)
dateCT = date(2015,11,3) # inaccurate

allc = curvesKeyword(allcurves, name = keyword) 
allc2 = curvesKeyword(allcurves, name = keyword2)
allc += allc2
#allc = curveCreation(date.today(), ['data/EJ_20160328_air_SPN4.csv'], verbose = 1)
refc = curvesKeyword(refcurves, name = refkeyword) 
cref = refc[refnum]


fig, (ax1, ax2) = pyt.subplots(2,1, sharex=True, gridspec_kw=shr,figsize = (8,8))
tLabel = 'Transmission' if t is not None else 'Absorption'
fig.suptitle('EJ200SP samples '+tLabel+' Spectrum on 4Apr (Day 10)', y=.95, size=17)
iterfarb = iter(farben)
if showRef:
	lbl = cref.nametag #str(c.datetag)
	ax1.plot(x[s],cref.avgcurve(t=t)[s], label = 'Ref ' + lbl,
			 color = iterfarb.next())

lblarray = ['1P @3+4Mrad', '1P @  3Mrad', 
				'2P @3+4Mrad', '2P @  3Mrad', ]

for i,c in enumerate(allc):
	clr = iterfarb.next()
	lbl = c.label(nslice = slice(6,None)) 
	#lbl = lblarray[i]
	ax1.plot(x[s],c.avgcurve(t=t)[s], label = lbl, color = clr)

ax1.plot(x[s],allc[0].errcurve(t=t)[s]*10, label = 'Error x10', color = 'cyan')
ax1.grid(True)
ax1.legend(loc = 0)
ax1.set_xlabel('Wavelength nm')
ax1.set_ylabel(tLabel)

#avgpcterr = np.sqrt(sum([c.errcurve()**2 for c in allc]))/sum([c.avgcurve() for c in allc])
avgpcterr = np.abs(cref.errcurve(t=t))/cref.avgcurve(t=t)
# to show diff in absp plots
if (not t) and df:
	avgpcterr = np.abs(cref.errcurve(t=t))
#avgpcterr = sum([np.abs(c.errcurve(t=t))/c.avgcurve(t=t) for c in allc])/len(allc)
ax2.fill_between(x[s],-avgpcterr[s],avgpcterr[s], label = 'err',alpha = .3) #default .2
iterfarb = iter(farben)
if showRef:
	iterfarb.next()
for c in allc:
	if (not t) and df:
		ax2.plot(x[s],(c.avgcurve(t=t)-cref.avgcurve(t=t))[s], color = iterfarb.next())
	else: 
		ax2.plot(x[s],(c.avgcurve(t=t)/cref.avgcurve(t=t)-1)[s], color = iterfarb.next())

ax2.grid(True)
ax2.set_xlabel('Wavelength nm')
ax2.set_ylabel('Diff' if (not t) and df else 'Ratio-1')
pyt.show(block = False)

