import numpy as np
import matplotlib.pyplot as pyt
from datetime import date
from Curve import Curve, curvesKeyword, curveCreation, specPlotter,curvesAge, curvesRef, readCurveFile

## compare curves of the same age of irradiation
curves = readCurveFile('measuredates_new.txt', verbose = 1, skips = 1) 


farben = ['blue', 'green', 'red' , 'blueviolet','slategray','darkcyan','magenta']
farben += ['hotpink', 'salmon','springgreen','chocolate', 'crimson']

#pyt.figure(figsize = (8,5))
x= np.linspace(600,200,401)
s = Curve.makeslice(350,550)		#slice(None) # x-range (band of wavelength in nm)
t = True
refnum = 0
daysIrr = 7
coldwarm = True
legFont = 13

# plot all curves of material A and day of irradaition D
keyword = '200-1X'
ckeyword = curvesKeyword(curves, char = '-', name = keyword)
allc = curvesAge(ckeyword, day = daysIrr, rincl = False, dayrange = 1)
cref = curvesRef(ckeyword, rred=False) 
print cref
#specPlotter(c1, 'EJ260-1X1P on day 24', xlabel='wavelength nm', ylabel='transmission', trsm=1)
batchDes = ['', ' UnIrr.', 'N2 @3Mrad', 'N3 @3Mrad High Rate', 'N4 @3Mrad $N_{2}$', 'CastorT'] 
if coldwarm:
	batchDes = ['', ' UnIrr.']+ [0]*7 +[' UnIrr.', r'23$^{\circ}$C', r'-30$^{\circ}$C'] 


fig, (ax1, ax2) = pyt.subplots(2,1, sharex=True, gridspec_kw=dict(height_ratios = [3,2]),figsize = (8,8))
tLabel = ' Transmission' if t is not None else ' Absorption'
fig.suptitle('EJ'+ keyword+ tLabel +' Spectrum', y=.95, size=17)
iterfarb = iter(farben)
ax1.plot(x[s],cref[refnum].avgcurve(t=t)[s], label = 'Unirradiated ',
			 color = iterfarb.next())
for c in allc:
	clr = iterfarb.next()
	lbl = (c.label(nslice = slice(0,-3),dslice = slice(0,0))+' '+batchDes[c.batch])
	ax1.plot(x[s],c.avgcurve(t=t)[s], label = lbl, color = clr)
ax1.plot(x[s],allc[0].errcurve(t=t)[s]*10, label = 'Error x10', color = 'cyan')
ax1.grid(True)
ax1.legend(loc = 0, fontsize = legFont)
ax1.set_xlabel('Wavelength nm')
if t is None:
	ax1.set_ylabel('Absorption')
else:
	ax1.set_ylabel('Transmission')

#avgpcterr = np.sqrt(sum([c.errcurve()**2 for c in allc]))/sum([c.avgcurve() for c in allc])
avgpcterr = np.abs(cref[refnum].errcurve(t=t))/cref[refnum].avgcurve(t=t)
#avgpcterr = sum([np.abs(c.errcurve(t=t))/c.avgcurve(t=t) for c in allc])/len(allc)
ax2.fill_between(x[s],-avgpcterr[s],avgpcterr[s], label = 'err',alpha = .2)
iterfarb = iter(farben)

iterfarb.next()
for c in allc:
	ax2.plot(x[s],(c.avgcurve(t=t)/cref[refnum].avgcurve(t=t)-1)[s], color = iterfarb.next())


ax2.grid(True)
ax2.set_xlabel('Wavelength nm')
ax2.set_ylabel('Ratio -1')
pyt.show(block = False)



