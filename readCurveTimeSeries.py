## readCurveTime obsolete as the 370 dip/ peak irrelevant
## step: plot the location of step instead of transmission level
## 07/04/2016: extend functionality to include wider range of time series
## Last mod: 07/04/2016

import numpy as np
import matplotlib.pyplot as pyt
from datetime import date
from Curve import (Curve, curvesKeyword, curveCreation, keycGen,
		readCurveFile, curvesAge, curvesRef)
from Curve_TimeFit import Curve_TimeFit

##  Set-up parameters
#curves = readCurveFile('measuredates.txt', verbose = 1, skips =1) 
curves = readCurveFile('measuredates_new_ref.txt', verbose = 1, skips =1) 
curves += readCurveFile('measuredates_June.txt', verbose = 1, skips =1) 
cKeyword = 'EJ260-1X1P N1'
sample2 = False
cKeyword2= ''
eb = True #error bar
errvy = 1 # error every
mk = '' #'2P ' 			# additional label for second group of samples
newdate = False
coldwarm = False
threesteps = True 		# Measure multiple steps in EJ260 1X1P -- for calibration
isMemplot = False 		# Plot member functions

figarg = dict(figsize = (12,8))
fx = lambda c: Curve_TimeFit.steplocTrsmQuad(c) # plotting fx
#fx2 = lambda c: steplocTrsmQuad(c) #, lmbShift = -64.94)
fx2 = lambda c : Curve.valueat(c, 425) # plotting function
yaxis = 'Step wavelength (nm)'
#yaxis = 'Deviation wavelength (nm)'
#yaxis = r'Transmission Coeff. (0< $\tau$ <1)'
#titleword = ' Deviation in transmittance step (trsm = 0.7)'
#titleword = ' Transmission Step (trsm = 0.7)'
titleword = r' Transmission Coeff.'

farben2 = ['lightskyblue', 'greenyellow', 'lightsalmon', 'violet', 'cyan','blueviolet', 'darkcyan']
farben2 +=['darkblue', 'darkgreen', 'darkred', 'darkmagenta', 'darkcyan']
farben= ['blue', 'green', 'red', 'magenta', 'cyan'] ##**
farben += ['hotpink', 'salmon','slategray','springgreen','chocolate', 'crimson']
farbiter = iter(farben)
farb2iter = iter(farben2)






# description/ designation of each batch
batchDes = ['', ' UnIrr.', 'N2 @3Mrad', 'N3 @3Mrad High Rate', 'N4 @3Mrad $N_{2}$', 'CastorT'] 
batchDes2 = ['', ' UnIrr.', 'N2 @3+4Mrad', 'N3 @3Mrad High Rate', 'N4 @4Mrad', 'CastorT'] 
batch = ['','N1', 'N2', 'N3', 'N4']
batchnum = None

x= np.linspace(600,200,401)
dateN = [0, date(2015,12,19), date(2015,12,19), date(2016,01,14), date(2016,01,11)]
if newdate:
	dateN[1] = date(2016,01,30) # arbitrary date: for compactness's sake
	dateN[2] = dateN[4] = date(2016,03,25)
#dateCT = date(2015,11,3) # inaccurate
datecold , datewarm = date(2016,04,01), date(2016,04,04)
dateN = [date(2016,01,11)]*5 # TO UNDO ORDER BY IRR DATE
if coldwarm:
	batchDes = ['', ' UnIrr.', '23$^{\circ}$C', '-30$^{\circ}$C', 'N4 @4Mrad', 'CastorT'] 
	batch = ['', '', '10', '11', 'N4']
	batchnum = [None, 9, 10, 11, None]
	dateN[1] = dateN[3] = datecold
	dateN[2] = datewarm

#print batchnum
keycurve, keycN = keycGen(curves, cKeyword, batch, batchnum=batchnum)
if sample2:
	key2curve, key2cN = keycGen(curves, cKeyword2, batch, batchnum)


print 'reference samples set: ', keycN[1]
fig0 = pyt.figure(**figarg)
if eb:
	plotfunction = pyt.errorbar
else:
	plotfunction = pyt.plot
if sample2:
	if key2cN[1]:
		plotfunction(*Curve_TimeFit.maketimegraph(key2cN[1],dateN[1], errbar = eb, fx = fx2), linestyle = 'dashed', linewidth = 1.3 , 
			label = key2cN[1][-1].nametag[:-3] + batchDes2[1],marker='D', color = farb2iter.next())
	else: 
		raise RuntimeError('No reference sample matches keyword')
	for i in [2,3,4]:
		if key2cN[i]:
			plotfunction(*Curve_TimeFit.maketimegraph(key2cN[i],dateN[i], errbar = eb, fx = fx2),linestyle = 'dashed', linewidth = 1.6, 
				label = mk+ batchDes2[i], marker='o', color = farb2iter.next())#, errorevery = errvy)

#plotfunction([1.],steploc(keycN[1][0], lambdapt), yerr = keycN[1][0].errcurve()[600 - lambdapt] , label = 'N1', lw = 2, capsize = 5)
if isMemplot:
	# makes plot of member Time Series
	tgdata = [0]*5
	for i in range(1,5):
		fxm = lambda c: steplocTrsmQuadMem(c, i, avging = False, step = .7, verbose=True) # taking average
		#fxm = lambda c: Curve.valueat(c,550, side = i)
		tgdata[i] = Curve_TimeFit.maketimegraph(keycN[1], dateN[1], errbar = eb, fx=fxm)
		print ' side '+' abcd'[i], np.average(tgdata[i][1])
		# plot horizontal line (optional)
		pyt.axhline(y=np.average(tgdata[i][1]), linewidth = 1.3, color = farb2iter.next(), linestyle = 'dashed')
	for i in range(1,5):
		plotfunction(*tgdata[i], marker = '.',linewidth = 1.3, color = farbiter.next(), linestyle='None',
				label = keycN[1][-1].label()[:-5] + ' side '+' abcd'[i])
else:
	if keycN[1]:
		plotfunction(*Curve_TimeFit.maketimegraph(keycN[1],dateN[1], errbar = eb, fx = fx,avging=True), linewidth = 1.3 , 
			label = keycN[1][-1].nametag[:-2] + batchDes[1],marker='D', linestyle='None', color = farbiter.next())
	else: 
		raise RuntimeError('No reference sample matches keyword')
	for i in [2,3,4]:
		if keycN[i]:
			plotfunction(*Curve_TimeFit.maketimegraph(keycN[i],dateN[i], errbar = eb, fx = fx), linewidth = 1.6, 
				label = batchDes[i], marker='o', color = farbiter.next())#, errorevery = errvy)

if threesteps:
	fx0 = lambda c:Curve_TimeFit.steplocTrsmQuad(c, poslope = False, step = .12, sample = 4, start = 200)
	tgdata = Curve_TimeFit.maketimegraph(keycN[1],dateN[1], errbar = eb, fx = fx0)
	avgp = np.average(np.array(tgdata[1]))
	tgdata[1] = [i - avgp for i in tgdata[1]]
	plotfunction(*tgdata, linewidth = 1.3, label = r't=.12 $_{avg}\lambda$ = %.1f' %avgp ,
		marker='D', linestyle='None', color = farbiter.next())

	fx1 = lambda c: Curve_TimeFit.steplocTrsmQuad(c, poslope = True, step = .12, sample = 4, start = 230)
	tgdata = Curve_TimeFit.maketimegraph(keycN[1],dateN[1], errbar = eb, fx = fx1)
	avgp = np.average(np.array(tgdata[1]))
	tgdata[1] = [i - avgp for i in tgdata[1]]
	plotfunction(*tgdata, linewidth = 1.3, label = r't=.12 $_{avg}\lambda$ = %.1f' %avgp 
		,marker='D', linestyle='None', color = farbiter.next())



pyt.grid(True)
pyt.legend(loc=0)
#pyt.xlabel('Days from Irradiation')
pyt.xlabel('Days (arbitrary)')
pyt.ylabel(yaxis)
lbl2 = ' and '+ cKeyword2 if sample2 else ''
pyt.title('EJ'+ cKeyword +lbl2+ titleword)
#fig0.get_axes()[0].set_ylim((0.86,0.92))
pyt.show(block = False)


