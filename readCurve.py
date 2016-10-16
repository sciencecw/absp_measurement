import numpy as np
import matplotlib.pyplot as pyt
from datetime import date

##		 readCurve.py
##	 	 general purpose program to plot a section of curves
##		 

x= np.linspace(600,200,401)

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
		return np.average(np.array(nonzero),0)

	def avgtcurve(self):
		# average transmission curve
		nonzero = self.nonzerodata()
		return np.average(np.power(10,(-1*np.array(nonzero))),0)

	def errcurve(self):
		# average error curve
		nonzero = self.nonzerodata()
		return np.ptp(np.array(nonzero),0)	

	def errtcurve(self):
		# average transmission error
		nonzero = self.nonzerodata()
		t= np.power(10,(-1*np.array(nonzero)))
		return np.ptp(t,0)/2

	def plotallcurves(self):
		i = 0
		for c in self.data:
			if c is not 0:
				pyt.plot(x, c, label = 'side '+(' ABCD'[i]))
			i+=1
		defaultplotting(self.nametag + ' ' + str(self.datetag))
		return


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

farben = ['blue', 'green', 'red', 'cyan', 'magenta', 'blueviolet', 'darkcyan']
farben += ['hotpink', 'salmon','slategray','springgreen','chocolate', 'crimson']

def defaultplotting(title, xlabel='wavelength nm', ylabel='absorption', hasGrid = True):
	pyt.grid(hasGrid)
	pyt.legend(loc = 0)
	pyt.xlabel(xlabel)
	pyt.ylabel(ylabel)
	pyt.title(title)
	pyt.show()
	return


def specPlotter(curves, title, xlabel='wavelength nm', ylabel='absorption'):
	# provided a set of curves, plot them with titles and legends as nametag of the curve
	for i in range(len(curves)):
		pyt.plot(x[:250],curves[i].avgcurve()[:250],label = curves[i].nametag, color = farben[i%len(farben)])
		#pyt.plot(x,curves[i].avgcurve(),label = curves[i].nametag, color = farben[i%len(farben)])
	defaultplotting(title, xlabel, ylabel, hasGrid = True)
	return

def curvesKeyword(icurves, name = None):
	if name is None:
		return icurves
	return [c for c in icurves if c.hasKeyword(name.split())]

# fixed parameters
## date of irradiation
dateN2 = date(2015,12,19)
dateN3 = date(2016,01,14)
dateN4 = date(2016,01,11)



## configure files to read

#cdate = date(2016,01,12)
#filenames = ['data/EJ200_EJ260_20160112.csv', 'data/EJ260-4X4P_20160112.csv', 'data/EJ260-1X1P_20160112.csv']
#curves = curveCreation(cdate, filenames)
#cdate = date(2016,01,18)
#filenames = ['data/EJ_20160118.csv']
#curves2 = curveCreation(cdate, filenames)
#curves = curves2
cdate = date(2016,01,29)
filenames = ['data/EJ_20160129.csv']
curves3 = curveCreation(cdate, filenames)
curves = curves3
#curves3 += curves2



## actual plotting

keycurve = curvesKeyword(curves, name = '260') 
pyt.figure(figsize = (8,6))
specPlotter(keycurve, 'Plastic Scintillator Absortion Spectrum '+str(cdate), ylabel = 'transmittion')
#specPlotter(keycurve, 'Plastic Scintillator Absortion Spectrum 18,29Jan 2016')



