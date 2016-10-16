## readCurveTime obsolete as the 370 dip/ peak irrelevant

import numpy as np
import matplotlib.pyplot as pyt
from datetime import date



class Curve:
	
	def __init__(self,name,date):
		self.nametag = name
		self.datetag = date
		self.data = [0]*5
		print self.nametag

	def __repr__(self):
		return '<'+self.nametag+'>'

	def add(self, number, dcurve):
		self.data[number] = dcurve

	def view(self, number):
		return self.data[number]

	def hasKeyword(self, keywords):
		isTrue = True
		for keyword in keywords:
			isTrue = isTrue and (keyword in self.nametag)
		return isTrue

	def nonzerodata(self):
		return np.array([x for x in self.data if x is not 0])

	def avgcurve(self):
		nonzero = self.nonzerodata()
		return np.average(np.power(10,(-1*np.array(nonzero))),0)

	def errcurve(self):
		nonzero = self.nonzerodata()
		return np.std(np.power(10,(-1*np.array(nonzero))),0)	 # need to fix this	


def curveCreation(cdate, filenames):
	tempcurve = []
	for fname in filenames:
		f = open(fname)
		names = f.readline().split(',')
		names = names[0::2]
		f.close()
		f2 = np.loadtxt(fname,skiprows = 2,delimiter = ',')

		lastname = ''
		for i, n in enumerate(names):
			truename = n[:-1]
			if truename != lastname:
				tempcurve.append(Curve(truename,cdate))
				lastname = truename
			tempcurve[-1].add(ord(n[-1])-96,f2[:,i*2+1])
		print fname
	return tempcurve

cdate = date(2016,01,12)
filenames = ['data/EJ200_EJ260_20160112.csv', 'data/EJ260-4X4P_20160112.csv', 'data/EJ260-1X1P_20160112.csv']
curves = curveCreation(cdate, filenames)
cdate = date(2016,01,18)
filenames = ['data/EJ_20160118.csv']
curves2 = curveCreation(cdate, filenames)
cdate = date(2016,01,29)
filenames = ['data/EJ_20160129.csv']
curves3 = curveCreation(cdate, filenames)
cdate = date(2016,02,04)
filenames = ['data/EJ_20160204.csv']
curves4 = curveCreation(cdate, filenames)
cdate = date(2016,02,07)
filenames = ['data/EJ_20160207.csv']
curves5 = curveCreation(cdate, filenames)
curves = curves+curves2+curves3+curves4+curves5


farben = ['blue', 'green', 'red', 'cyan', 'magenta', 'blueviolet', 'darkcyan']
farben += ['hotpink', 'salmon','slategray','springgreen','chocolate', 'crimson']

x= np.linspace(600,200,401)

def specPlotter(curves, title, xlabel='wavelength nm', ylabel='absorption' ):
	for i in range(len(curves)):
		print i
		pyt.plot(x,curves[i].avgcurve(),label = curves[i].nametag, color = farben[i%len(farben)])
	pyt.grid(True)
	pyt.legend(loc =0)
	pyt.xlabel(xlabel)
	pyt.ylabel(ylabel)
	pyt.title(title)
	pyt.show()
	return

def curvesKeyword(icurves, name = None):
	if name is None:
		return icurves
	return [c for c in icurves if c.hasKeyword(name.split())]

keycurve = curvesKeyword(curves, name = '200 1X') 
keycN1 = curvesKeyword(keycurve, name = 'N1') 
keycN2 = curvesKeyword(keycurve, name = 'N2') 
keycN3 = curvesKeyword(keycurve, name = 'N3') 
keycN4 = curvesKeyword(keycurve, name = 'N4') 

dateN2 = date(2015,12,19)
dateN3 = date(2016,01,14)
dateN4 = date(2016,01,11)

lambdapt = 425 #nm wavelength of interest

def mingen(c):
	ac = c.avgcurve()[200:250]
	acpeak = np.argmin(ac)
	print acpeak
	acmin = np.average(ac[acpeak-4:acpeak+4])
	return acmin

def valueat(c, lbd):
	return c.avgcurve()[600-lbd]

def maketimegraph(keyc, radiation_date):
	days = []
	pvalue = []
	for c in keyc:
		days.append((c.datetag- radiation_date).days)
		pvalue.append(valueat(c, lambdapt))
	return [days, pvalue]

print 'should have only one sample: ', keycN1
pyt.figure(figsize = (8,5))
pyt.errorbar([1.],valueat(keycN1[0], lambdapt), yerr = keycN1[0].errcurve()[600 - lambdapt] , label = 'N1', lw = 2, capsize = 5)
pyt.plot(*maketimegraph(keycN2,dateN2), label = 'N2',marker='o')
pyt.plot(*maketimegraph(keycN3,dateN3), label = 'N3',marker='o')
#pyt.plot(*maketimegraph(keycN4,dateN4), label = 'N4',marker='o')
pyt.grid(True)
pyt.legend(loc=0)
pyt.xlabel('days from irradiation')
pyt.ylabel('transimission (at 425nm)')
pyt.title('EJ200-1X transimission spec over time')
pyt.show()

#pyt.errorbar([1.],mingen(keycN1[0]), yerr = keycN1[0].errcurve()[234] , label = 'N1', capsize = 5)
#pyt.show()



#pyt.plot(x,curves[i].avgcurve(),label = curves[i].nametag, color = farben[i%len(farben)])
#pyt.figure(figsize = (12,7))
#specPlotter(keycurve, 'Plastic Scintillator Absortion Spectrum '+str(cdate), xlabel = 'Days from irradiation')
#specPlotter(keycurve, 'Plastic Scintillator Absortion Spectrum 18,29Jan 2016')



