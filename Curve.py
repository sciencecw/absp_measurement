import numpy as np
import matplotlib.pyplot as pyt
import os
from datetime import date

##
##		 # Curve.py #
##	 	 General purpose functions to read absorption spectrum file
##			prepared: 05/02/2016 by Kak Wong
##			last edit: 09/07/2016
##		 


## date of irradiation
dateN2 = date(2015,12,19)
dateN3 = date(2016,01,14)
dateN4 = date(2016,01,11)
dateN4new = date(2016,03,25)
dateCT = date(2015,11,3) # inaccurate

datecold = date(2016,04,01)
datewarm = date(2016,04,04)


class Curve:
	""" Absorption Curve Class """
	x= np.linspace(600,200,401)
	# irradation date of batch array
	dN = [0,0,dateN2,dateN3,dateN4,0,dateN4new,0,dateN4new,
			0, datewarm,datecold]+[0]*2
	# useful colors on matplotlib
	farben = ['blue', 'green', 'red', 'magenta', 'blueviolet', 'darkcyan']
	farben += ['hotpink', 'salmon','slategray','springgreen','chocolate', 'crimson']
	irrdates = dict()
	# verbose trigger
	verbose = 0
	


	## CONSTRUCTOR
	def __init__(self, name, date, silent = False):
		""" Curve class CONSTRUCTOR """
		## note: castor table not given a batch num yet
		self.nametag = name
		self.datetag = date
		self.data = [0]*5
		try:
			i = self.nametag.index('-N')
			self.batch = int(self.nametag[i+2])
		except ValueError:
			self.batch = 0
		# special line for new irradiation
		if (self.batch in [2,4] and 'EJ200SP' in self.nametag
					and self.datetag >= dateN4new):
			self.batch +=4
		# EJ200 irradiation
		if (self.batch == 0 and self.hasKeyword(['EJ200','1X-'])):
			self.coldsamples()
		if ('EJ' in self.nametag) and ('PVT' in self.nametag):
			i = self.nametag.index('P-N')
			self.batch = int(self.nametag[i+3:])+20
		if ('EJ' in self.nametag) and ('PS' in self.nametag):
			i = self.nametag.index('P-')
			self.batch = int(self.nametag[i+2:])+20
		if Curve.verbose == 1 and not silent:
			#print self.batch, ': ', self.nametag, self.cvage()
			print "%-15s %s %s" %(self.nametag, self.batch, self.cvage())

	# subroutine for warm/cold samples
	def coldsamples(self):
		i = self.nametag.index('X-')
		try:
			number = int(self.nametag[i+2:i+4])
		except ValueError:
			number = int(self.nametag[i+2:i+3])
		if number == 10 or number == 11:
			self.batch = number
		else:
			self.batch = 9
		return

	def __repr__(self):
		return '<'+self.nametag+' '+''.join(['_' if d is 0 else 'o' for d in self.data[1:5]])+str(self.__len__())+'>'

	## INPUT CURVE DATA
	def add(self, number, dcurve):
		if self.data[number] is not 0:
			self.data.append(dcurve)
			#print 'extra data curve!'
		else:	
			self.data[number] = dcurve

	## BASIC FUNCTION
	def __len__(self):
		return self.nonzerodata().__len__()
	def len(self):
		return self.__len__()
		
	def view(self, number, t = None):
		if t: return self.viewt(number)
		return self.data[number]
	
	def viewt(self, number):
		if self.data[number] is 0:
			return 0
		return Curve.trsm(self.data[number])

	def printType(self):
		return [type(d) for d in self.data]

	def hasKeyword(self, keywords):
		isTrue = True
		if type(keywords) == str:
			keywords = [keywords]
		for keyword in keywords:
			isTrue = isTrue and (keyword in self.nametag)
		return isTrue

	def arraynzd(self):
		return np.array(self.nonzerodata())
	def nonzerodata(self):
		return [x for x in self.data if x is not 0]

	def label(self, nslice = slice(None), dslice = slice(5, None), hasDay=True):
		lbl = self.nametag[nslice] + ' ' + str(self.datetag)[dslice] 
		if hasDay:
			age = self.cvage()
			if age != -1:
				lbl = lbl +' Day '+str(age)
		if '-6' in self.nametag and self.batch == 6:
			lbl = 'CasT ' + lbl
		return lbl

	def cvage(self):
		""" age of a sample from last irradiation """
		try:
			age = (self.datetag - Curve.dN[self.batch]).days
		except (TypeError, IndexError):
			age=-1
		for piece in Curve.irrdates.keys():
			if self.hasKeyword(piece):
				age = (self.datetag - Curve.irrdates[piece]).days
				return age
		return age
	
	## STATIC METHOD
	@staticmethod
	def valueat(c, lbd, side = 0):
		if side > 0:
			t = Curve.trsm(c.data[side])
			# exception: if side curve is missing. raise error code 0 so maketimegrpah can catch it
			if type(t) is not np.ndarray and t == 1:
				raise ValueError(0,c.label()+'side '+' abcd'[side]+' is empty')
			return t[600-lbd]
		print 'lambda=', lbd,'nm: ', c.avgcurve()[600-lbd]
		return c.avgtcurve()[600-lbd], c.errtcurve()[600-lbd]

	@staticmethod
	def trsm(absp):
			return np.power(10,(-1.*np.array(absp)))
	@staticmethod
	def absp(trsm):
			return -np.log10(np.array(trsm))

	@staticmethod
	def ctypename(t = None): #default typename is absorption
		return 'Transmission' if t else 'Absorption'

	@staticmethod
	def makeslice(a,b):
		""" slicing generator: converts 200-600nm to python index """
		return slice(600-b,600-a)

	@staticmethod
	def defaultplotting(title = None, xlabel='wavelength nm', axis = 0, ylabel=None, 
								hasGrid = True, t=None, block = True, isShow = True):
		## default plotting
		if not axis: axis = pyt
		else: axis.xlabel, axis.ylabel = axis.set_xlabel, axis.set_ylabel
		if not ylabel: ## if ylabel not specified
			ylabel = Curve.ctypename(t)
		axis.grid(hasGrid)
		#axis.legend(loc = 0)
		axis.xlabel(xlabel)
		axis.ylabel(ylabel)
		if title: axis.title(title)
		if isShow: axis.show(block = block)
		return

	@staticmethod
	def compPlotter(ax_main, ax_ratio,xx, avg, ref, lw1 = 1, lw2 = 1, yexp = None, **kwargs):
		""" Plotter defined for the Comparison graph """
		ax_main.plot(xx,avg, linewidth = lw1, **kwargs)
		if yexp:
			y = eval(yexp)
		else: 
			y = (avg/ref-1)
		ax_ratio.plot(xx,y, linewidth = lw2, **kwargs)

	@staticmethod
	def compSidePlotter(ax_main, ax_ratio,xx, c, cref, lw1 = 1., lw2 = 1 , s=slice(None)):
		""" Plot two pieces and compare their individual sides """
		for i in range(1,5):
			clr, lbr = Curve.farben[i-1], ' side '+ ' ABCD'[i]
			if cref.viewt(i) is not 0:
				ax_main.plot(xx[s], cref.viewt(i)[s], linewidth = lw1, 
					color = clr, label = cref.label() + lbr, linestyle = 'dashed')
			if c.viewt(i)[s] is not 0:
				ax_main.plot(xx[s], c.viewt(i)[s]   , linewidth = lw1, 
					color = clr, label = c.label()+lbr)
			if cref.viewt(i) is not 0 and c.viewt(i) is not 0:
				y = c.viewt(i)/cref.viewt(i) -1
				ax_ratio.plot(xx[s],y[s], linewidth = lw2,color = Curve.farben[i-1])
			else:
				print 'ref curve:curve Side', ' ABCD'[i],type(cref.viewt(i)), type(c.viewt(i))
		Curve.defaultplotting(axis = ax_main ,isShow = False)
		Curve.defaultplotting(axis = ax_ratio , ylabel = 'Ratio-1', isShow = False)
		return

	## SUBCLASS
	class NoneIter:
		""" None Iterater """
		def __init__(self):
			print "initiate None iterater"
		def next(self):
			return None

	## PRODUCE CURVES
	def avgcurve(self, t=None):
		if t:
			return self.avgtcurve()
		nonzero = self.arraynzd()
		return np.average(np.array(nonzero),0)

	def avgtcurve(self):
		# average transmission curve
		nonzero = self.arraynzd()
		#return np.max(self.trsm(nonzero),0)
		return np.average(self.trsm(nonzero),0)

	def mvavgtcurve(self, n=3):
		nzd = self.nonzerodata()
		for i in range(len(nzd)):
			nzd[i]= Curve.moving_average(self.trsm(nzd[i]), n=n)
		return np.average(np.array(nzd),0)

	def errcurve(self, t=None):
		# average error curve
		if t:
			return self.errtcurve()
		nonzero = self.arraynzd()
		#return np.ptp(np.array(nonzero),0)/2	
		return np.std(np.array(nonzero),0)	

	def errtcurve(self):
		# average transmission error
		nonzero = self.arraynzd()
		t= self.trsm(nonzero)
		#t= np.power(10,(-1*np.array(nonzero)))
		#return np.ptp(t,0)/2
		return np.std(t,0)

	def diff(self,refl_reduction = False):
		a = self.view(2)+self.view(4)
		b = self.view(1)+self.view(3)
		if refl_reduction:
			a=a-a[20:80].sum()/60
			b=b-b[20:80].sum()/60
		return (a-b)/(a+b)

	@staticmethod
	def diffc(c1,c2):
		a = c1.avgcurve()
		b = c2.avgcurve()
		return (a-b)/(a+b)

	@staticmethod
	def moving_average(a, n=3) :
	    ret = np.cumsum(a, dtype=float)
	    ret[n:] = ret[n:] - ret[:-n]
	    return ret[n - 1:] / n


	# CURVE GENERATORS
	def addCurve(self, c):
		""" Combine two Curve objects """
		self.data.extend(c.nonzerodata())

	def copy(self):
		c = Curve(self.nametag, self.datetag, True) # silent
		c.data = [0]*len(self.data)
		for i, e in enumerate(self.data):
			if e is not 0:
				c.data[i] = np.copy(e)
		return c

	def __add__(self, other):
		""" built-in add function """ 
		c = self.copy()
		c.addCurve(other)
		return c

	def __radd__(self, other):
		""" built-in reverse add function """
		if other == 0: 
			return self.copy()
		else: 
			return self.__add__(other)

	@staticmethod
	def shifter(ar, shift = 0.5):
		""" return curve with shifted x axis 
			using linear extrapolation """
		## left shift case
		if shift > 0:
			iShift = int(np.ceil(shift)-1)			# integer shift
			deci = shift - iShift		# decimal part
			## special case where deci = 0??? ##TODO!
		 	newar = np.convolve(ar, [deci, 1- deci] + [0]*iShift, 'valid')
		 	return np.append(newar, [np.nan]*(iShift+1)) # padding for x
		# right shift
		if shift <=0:
		 	shift = -shift
		 	iShift = int(np.ceil(shift) - 1)
		 	deci = shift - iShift
		 	newar = np.convolve(ar,  [0]*iShift + [1- deci ,deci] , 'valid')
		 	return np.append([np.nan]*(iShift+1), newar)	

	@staticmethod	 	
	def readIrrDate(logfile):
		f = open(logfile)
		irrdates = dict()
		for line in f:
			s = line.rstrip().split(',') 
			if '#' not in s[0]:# skip comment lines 
				try: # first three items: date of measurement
					cdate = date(*map(int,s[:3]))
				except ValueError:
					print 'error:',s 
					raise
				# follows: filenames
				piecename = [piece.lstrip(" '").rstrip(" '\n") for piece in s[3:]]
			irrdates.update([[p, cdate] for p in piecename])
		print irrdates
		return irrdates

	## PLOTTING FUNCTIONS
	def plot(self, t=None):
		pyt.plot(Curve.x,self.avgcurve(t))
		print self.label()
		Curve.defaultplotting(self.label(),t=t)
		return

	def plotallcurves(self, t=None, newfig = None, plotting = True):
		# plot all member curves of a measured piece 
		i = 0
		if newfig:
			fig = pyt.figure()
		for c in self.data:
			if c is not 0:
				if t:
					c = self.trsm(c)
				pyt.plot(Curve.x, c, label = 'Side '+(' ABCD1234567890'[i]))
			i+=1
		print self.label()
		if plotting:
			Curve.defaultplotting(self.nametag + ' ' + str(self.datetag),t=t, block = not newfig)
		return

	def plotallcurvesComp(self, t=None, plotting = True, s = slice(None),
			shr = dict(height_ratios = [3,2]),ratioyrange=None, save = False, showDiff = False):
		# always creates newfigure due to subplots
		fig, (ax1, ax2) = pyt.subplots(2,1, sharex=True, gridspec_kw=shr,figsize = (8,8))
		fig.suptitle(self.nametag + ' ' + str(self.datetag), y=.95, size=17)
		for i,c in enumerate(self.data):
			if c is not 0:
				if t:
					c = self.trsm(c)
				ax1.plot(Curve.x[s], c[s], label = 'Side '+(' ABCD1234567890'[i]))
				if not t:
					ax2.plot(Curve.x[s],(c-self.avgcurve(t=t))[s])
				else: 
					ax2.plot(Curve.x[s],(c/self.avgcurve(t=t)-1)[s])
		if showDiff:
			kwarg_Diff = dict(color = 'darkred', linestyle = 'dashed')
			ax1.plot([np.nan],[np.nan], label = 'Absp Diff', **kwarg_Diff)
			ax2.plot(Curve.x[s],self.diff, **kwarg_Diff)
		ax1.plot(Curve.x[s],self.errcurve(t=t)[s]*10, label = 'Error x10', color = 'cyan')
		Curve.defaultplotting(axis = ax1, t=t, isShow = False)
		ax1.legend(loc = 0)
		Curve.defaultplotting(axis = ax2, ylabel = 'Diff' if (not t) else 'Ratio-1', isShow = False)
		ax2.set_ylim(ratioyrange)
		print self.label()
		if plotting:
			pyt.show(block= True)
		if save:
			filen_init = 'plots/SpecCompMem'+self.nametag+'_'+str(self.datetag)[5:] 
			Curve.saveFigHelper(filen_init,fig)
			pyt.close()
		return

	### test of concept ###
	def plotallcurvesDiff(self, plotting = True, s = slice(None),
			shr = [3,2], save = False,ratioyrange=None, t=None):
		# always creates newfigure due to subplots
		# parameter t is ignored

		i = 0
		shr = dict(height_ratios = shr)
		fig, (ax1, ax2) = pyt.subplots(2,1, sharex=True, gridspec_kw=shr,figsize = (8,8))
		fig.suptitle(self.nametag + ' ' + str(self.datetag), y=.95, size=17)
		for i in range(1,5):
			c=self.view(i)
			if False: #c is not 0:
				ax1.plot(Curve.x[s], c[s], label = 'Side '+(' ABCD1234567890'[i]))
				ax2.plot(Curve.x[s],(c-self.avgcurve())[s],color =['gray','slategray'][i%2])
		a = self.view(2)+self.view(4)
		b = self.view(1)+self.view(3)
		#a=a-a[20:60].sum()/40+.005
		#b=b-b[20:60].sum()/40+.005
		ax1.plot(Curve.x[s], a[s], label = 'side B+D')
		#ax2.plot(Curve.x[s],(a-self.avgcurve())[s],color =['gray','slategray'][i%2])
		ax1.plot(Curve.x[s], b[s], label = 'side A+C')
		#ax2.plot(Curve.x[s],(b-self.avgcurve())[s],color =['gray','slategray'][i%2])
		#ax2.plot(Curve.x[s],self.diff(refl_reduction = True)[s],linestyle='dashed',linewidth=3)
		ax2.plot(Curve.x[s],((a-b)/(a+b))[s],linestyle='dashed',linewidth=3)
		ax1.plot(Curve.x[s],self.errcurve()[s]*10, label = 'Error x10', color = 'cyan')
		ax1.legend(loc = 0)
		defaultplotting(pyt = ax1, ylabel = 'Absorption', isShow = False)
		defaultplotting(pyt = ax2, ylabel = 'Diff', isShow = False)
		ax2.set_ylim(ratioyrange)
		print self.label()
		if plotting:
			pyt.show(block= True)
		if save:
			filen_init = 'plots/SpecCompMem'+self.nametag+'_'+str(self.datetag)[5:] 
			Curve.saveFigHelper(filen_init,fig)
			pyt.close()
		return

	@staticmethod
	def saveFigHelper(filen_init, fig):
		""" takes file name and save fig in png extension"""
		filen = filen_init + '.png'
		i=1
		while os.path.isfile(filen): 
			## wherein such filename exists, search for next available name
			filen = filen_init +'_'+str(i)+'.png'
			i+=1
		print 'saved: ' + filen
		fig.savefig(filen)
		return

	## remove spikes
	def spikeRm(self, value = 10.):
		d = [c for c in self.data if c is not 0]
		for c in d:
			while True:
				index = (c == value).nonzero()[0]
				if index.size < 1:
					break
				c[index] = c[index-1]
		return



def getAllCsv(path = 'data/'):
	farray = os.listdir(path)
	return [(path+f) for f in farray if f[-4:] == '.csv']

def readCurveFile(logfile, verbose = 1, skips = False, sepcurve =False):
	f = open(logfile)
	curves = []
	for line in f:
		s = line.rstrip().split(',')
		# skip comment lines
		if '#' not in s[0]: 
			# first three items: date of measurement
			try:
				cdate = date(*map(int,s[:3]))
			except ValueError:
				print 'error:',s 
				raise
			# follows: filenames
			filenames = [fn.lstrip(" '").rstrip(" '\n") for fn in s[3:]]
			curves+=curveCreation(cdate, filenames, 
							verbose = verbose, skips = skips, sepcurve = sepcurve)
	return curves

def curveCreation(cdate, filenames, verbose = 1, 
	skips = False, sepcurve = False, abspmode = True):
	#  skips: ignore unexpected entries and move on
	#		  default to False, which raises exceptions
	#  sepcurve: save entries into separate curves
	#  abspmode: if False, forces conversion to transmittances

	## read file and create curve class
	## return list of Curves
	tempcurve = []
	for fname in filenames:
		f = open(fname)
		if verbose:
			print fname
			Curve.verbose = 1
		names = f.readline().split(',')[0::2]
		modes = f.readline().rstrip('\n').rstrip('\r').split(',')[1::2]
		f.close()
		f2 = np.loadtxt(fname,skiprows = 2, delimiter = ',')

		lastname = ''
		for i, n in enumerate(names): 
			facenum = ord(n[-1])-96
			truename = n[:-1]
			inputcurve = True
			if facenum not in range(1,5):
				inputcurve = False
				if not skips: 	# not skipping/ skips = 0 
								## expects that each curve is importable
								## error is shown if that is not the case
					raise Exception('weird names: %s %s' % (n, ord(n[-1])-96))
				elif skips == 1: ## next input as new curve
					lastname = None
				elif skips == 3: ## inputs curve. Assumes "face a" 
					truename = n
					inputcurve = True
					facenum = 1
				elif skips == 2: ## completely ignore input (seldom needed)
					pass
				else:
					print '!exceptional case!', n, skips
					print 'treated as case II: complete ignores'
			if inputcurve:
				if truename != lastname or sepcurve:
					tempcurve.append(Curve(truename,cdate))
					lastname = truename
				if abspmode and modes[i] == 'Abs': 
				# even in default abspmode if the code detects T% it converts the number to absp
					tempcurve[-1].add(facenum,f2[:,i*2+1])
				else:
					tempcurve[-1].add(facenum,Curve.absp(f2[:,i*2+1]/100.))
					
	return tempcurve




## ACTION ON ARRAY OF CURVES
def curvesKeyword(icurves, name = None, char = None, batchn = None):
	""" given sample name string, return all curves contains the keyword """
	if name is None:
		return icurves
	if batchn is not None:
		return [c for c in icurves if c.hasKeyword(name.split(char)) and c.batch == batchn]
	return [c for c in icurves if c.hasKeyword(name.split(char))]

def curvesDate(icurves, date_measured):
	# return curves with the date
	# date can be date object or tuple
	if not date_measured:
		return icurves
	if type(date_measured) is tuple:
		date_measured = date(*date_measured)
	return [c for c in icurves if c.datetag == date_measured]

def curvesRemoveRedundant(icurves):
	temp = []
	for c in icurves:
		isNew = True
		for tc in temp:
			if tc.nametag == c.nametag:
				isNew = False
		if isNew:
			temp.append(c)
	return temp

def curvesAge(icurves, day = 0, rincl = False, dayrange = 0):
	""" return curves with a specific age of irradiation """
	ctemp = []
	for c in icurves:
		if c.batch <= 1 or c.batch == 9 :
			# case 1: option to include reference samples
			if rincl:
				ctemp.append(c)
		elif np.abs(c.cvage() - day) <= dayrange:
			# case 2-4: check irradaition date and datetag
			ctemp.append(c)
	return ctemp

def curvesRef(icurves, rred = False):
	# rred removes redundant options
	temp = [c for c in icurves if c.batch in [1,9] ]
	if rred:
		temp = curvesRemoveRedundant(temp)
	return temp

def keycGen(curves, cKeyword, keywords, batchnum=None, hasCastor = False):
	""" Similar to curvesKeyword: return curves with sample string
		Further selects for different batch numbers"""
	keycurve = curvesKeyword(curves, name = cKeyword) 
	keycN = [0]*5
	if not batchnum:
		batchnum = [None] * 5
	for i in range(5):
		keycN[i] = curvesKeyword(keycurve, name = keywords[i],batchn = batchnum[i]) 
	# Castor table samples are not of the same formula as the EJ200SP pieces
	#if hasCastor:
	#	keycN[5] = curvesKeyword(keycurve, name = '-6') 
	#else:
	#	keycN[5] = []
	return keycurve, keycN

def specPlotter(curves, title, xlabel='wavelength nm', ylabel='absorption', 
			target = pyt, xslice = (None,), t = 0):
	# provided a set of curves, plot them with titles and legends
	# as nametag of the curve
	s = slice(*xslice)
	for i in range(len(curves)):
		y = curves[i].avgcurve(t=t)
		target.plot(Curve.x[s],y[s],label = curves[i].nametag, 
				color = farben[i%len(farben)])
	Curve.defaultplotting(title, xlabel, ylabel, hasGrid = True, t=t)
	return





