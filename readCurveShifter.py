## adopted from readCurveTimeComp
## 12 July 2016 Kak

## to similate effects of shifted curves
import numpy as np
import matplotlib.pyplot as pyt
from datetime import date
import sys
from Curve import (Curve, curvesKeyword, curveCreation, keycGen,
					specPlotter,curvesAge, curvesRef, readCurveFile)

execfile('readCurveInput_default.py') # loads default setting

allcurves = curveCreation(date(2016,7,8),['data/EJ_20160708_air_test.csv'],
							verbose = 1, skips = 3,sepcurve=True)
			# separate curves are inputed

## selects only EJ260-1X1P... also only the a side measurements
allcurves = curvesKeyword(allcurves, name =  'EJ260-1X1P') [:27]
allcurves = [c for c in allcurves if c.view(1) is not 0]
cref = sum(allcurves[4:15])


farbGruppe = [['blue', 'darkblue','darkslateblue','royalblue', 'steelblue','darkcyan'],
			['red', 'darkred', 'crimson', 'orangered','salmon'],
			['green', 'darkgreen', 'olive', 'darkturquoise', 'greenyellow','sage'],
			['magenta','blueviolet','purple','darkmagenta','darkviolet'], 
			['slategray', 'dimgrey']]
farben = ['blue']+farbGruppe[1][:3]+farbGruppe[3][:4]

## Parameters 
s = Curve.makeslice(350,600) 	##x-range (band of wavelength in nm)
shr = dict(height_ratios = [2,3])		#subplot height ratio
figsize = (8,9)#(8,8)
legFont = 10				# legend font size
isBlocked = False			# Blocks interaction: if false the program should be run
							# with the tag "-i"


tLabel = 'Transmission' 	#if t else 'Absorption'
titleGen = r" 'EJ260-1X1P-N1 shifted in x' "
ratioyrange=[-0.06,0.06]
iterfarb =  iter(farben)



def avgshift_gen(c, shift):
	# local shorthand
	avg =  c.avgtcurve()#n=3)
	return Curve.shifter(avg, shift)


fig, (ax1, ax2) = pyt.subplots(2,1, sharex=True, gridspec_kw=shr,figsize = figsize)
fig.suptitle(eval(titleGen), y=.95, size=17)

# plot original curve
ref = cref.avgtcurve()[s]
Curve.compPlotter(ax1,ax2,x[s], ref, ref, 1.8, 1.8, None,
			 label = "original", linestyle ="solid")

## Plot shifted curves
for shift in [0.,.01,.05,.1,-.01,-.05,-.1]:
	lbl = "shifted %.2f nm" %shift
	Curve.compPlotter(ax1,ax2,x[s], avgshift_gen(cref, shift)[s] , ref, 1., 1.8, None,
			 color = iterfarb.next(), label = lbl, linestyle = "dashed")	


ax1.grid(True)
ax1.legend(loc = 0, fontsize = legFont)
ax1.set_xlabel('Wavelength nm')
ax1.set_ylabel('transmission')
ax2.grid(True)
ax2.set_xlabel('Wavelength nm')
ax2.set_ylabel('Ratio-1')
pyt.show(block = isBlocked)
