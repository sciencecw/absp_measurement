import numpy as np
import matplotlib.pyplot as pyt
from datetime import date

## written to compare curves from two different sampling days

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

	def hasKeyword(self,keywords):
		isTrue = True
		for keyword in keywords:
			isTrue = isTrue and (keyword in self.nametag)
		return isTrue

	def nonzerodata(self):
		return np.array([x for x in self.data if x is not 0])

	def avgcurve(self):
		nonzero = self.nonzerodata()
		#return np.average(np.array(nonzero),0)
		return np.average(10^(-1*np.array(nonzero)),0)

	def errcurve(self):
		nonzero = self.nonzerodata()
		return np.ptp(np.array(nonzero),0)		


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

farben = ['blue', 'green', 'red', 'cyan', 'magenta', 'blueviolet', 'darkcyan', 'hotpink', 'salmon','slategray']
pyt.figure(figsize = (12,7))
x= np.linspace(600,200,401)

curveNames = ['260 1X1P N1', '200 1X N2', '200 2X N2', '260 1X1P N2', '260 4X4P N2',
'200 1X N3', '260 1X1P N3', '200 2X N3', '260 4X4P N3','260 1X1P N4', '260 4X4P N4']
i = 0 
for name in curveNames:
	try:
		c1 = [c for c in curves if c.hasKeyword(name.split())][0]
		c2 = [c for c in curves2 if c.hasKeyword(name.split())][0]
		pyt.plot(x,c2.avgcurve()/c1.avgcurve(),label = c1.nametag, color = farben[i])
		print name, ' plotted'
		i+=1
	except IndexError:
		print name, ' does not exist in both sequences'

#for i in range(len(curves)):
##for i in range(2):
#	print i
#	pyt.plot(x,curves[i].avgcurve(),label = curves[i].nametag, color = farben[i])
pyt.grid(True)
pyt.legend()
pyt.xlabel('wavelength nm')
pyt.ylabel('absorption')
pyt.title('Scintillator absortion spectrum Ratio 18Jan to 12Jan')
pyt.show()



