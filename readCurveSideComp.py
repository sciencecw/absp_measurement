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
					specPlotter,curvesAge, curvesRef, readCurveFile)
from Curve_TimeFit import Curve_TimeFit

execfile('readCurveInput_default.py') # loads default setting
#execfile('readCurveInput_Oct_Normal.py')	
#execfile('readCurveInput_Oct_consistency.py')	

#allctemp = curveCreation(date(2016,10,14), 
#		['data/EJ_20161014_ameerruhikak.csv'], verbose = 1,skips=2)#, sepcurve=True)
#allctemp = curveCreation(date(2016,10,13), 
#		['data/EJ_20161013_kakandres.csv', 'data/EJ_20161013_kak_air.csv'], verbose = 1,skips=2)#, sepcurve=True)
refctemp = curveCreation(date(2017,3,16), 
		['data/EJ_20170316_air_sara_kak_verf.csv','data/EJ_20170316_air_kak.csv'], verbose = 1,skips=1)
#refctemp = readCurveFile('measuredates/measuredates_Oct.txt', verbose = 1, skips = 1)
allctemp = refctemp
#allctemp = curveCreation(date(2016,10,21), ['data/EJ_20161021-air_calib.csv'], verbose = 1,skips=2)
#curveCreation(date(2016,10,18), 
#		['data/EJ_10-18-2016-air_calib.csv'], verbose = 1,skips=2)


if False:
	def avg_gen(c):
		# local shorthand
		# *** Special: to cancel out effect of higher attenuation on C side ***
		nonzero = c.arraynzd()[(0,1,3),:]
		temp = np.average(c.trsm(nonzero),0)[s]
		return temp

keyword= refkeyword= sys.argv[1] #'EJ200SP-1P-N1'
allcurves = curvesKeyword(allctemp, name = keyword)
refcurves = curvesKeyword(refctemp, name = keyword)
print [c.len() for c in allcurves]
print [c.len() for c in refcurves]
print allcurves
print refcurves
cnum, refnum = 0, 1
s =  Curve.makeslice(350,600)
ratioyrange= [-0.06,0.06]

c_int = allcurves[cnum]
cref = refcurves[refnum]
fig, (ax1, ax2) = pyt.subplots(2,1, sharex=True, gridspec_kw=shr,figsize = (8,8))
## TITLES and labels
if baseline: print "Error: baseline setting"
fig.suptitle(eval(titleGen), y=.95, size=17)
# DRAW REFERENCE AND ERROR 
if showRef:
	lbl = 'Ref ' + cref.nametag if isOrigLabel else itercLabel.next()
	ax1.plot(x[s],avg_gen(cref), label = lbl, color = 'gray' ,linewidth = 1.8)
avgpcterr = np.abs(cref.errcurve(t=t))/cref.avgcurve(t=t)
if (not t) and df: 
	avgpcterr = np.abs(c_int.errcurve(t=t))
ax1.plot(x[s],allcurves[0].errcurve(t=t)[s]*10, label = 'side variation x10', color = 'cyan')
ax2.fill_between(x[s],-avgpcterr[s],avgpcterr[s], alpha = .2) 
	

ref = avg_gen(cref) #?? what is this for?
Curve.compSidePlotter(ax1,ax2,x, c_int, cref, s=s)

ax1.legend(loc = 0, fontsize = 10)
if t:
	ax1.set_ylim([0.,1.])
ax2.set_ylim(ratioyrange)
pyt.show(block = isBlocked)

#print 'interesting curve'
#x0,_ = Curve_TimeFit.steplocTrsmQuadMem2(c_int)
#print cref.datetag, x0
#print 'ref curves'
#for c in refcurves:
#    x0,_ = Curve_TimeFit.steplocTrsmQuadMem2(c)
#    #xarray.append(x0)
#    print c.datetag , x0-_10

#fig.savefig('plots/SpecCompPS-PVT-6_7/SpecComp'+refkeyword+'.png')
