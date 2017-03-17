##
##		 # Curve_TimeFit.py #
##	 	 general purpose functions to produce time series and fitting
##			prepared: 05/02/2016
##			last edit: 29/06/2016
##		 

import numpy as np
import matplotlib.pyplot as pyt
from Curve import Curve
from datetime import date
from scipy.optimize import curve_fit

class Curve_TimeFit:
	x = np.linspace(600,200,401)
 
	@staticmethod
	def maketimegraph(keyc, radiation_date, fx, errbar = True, avging = False):
		days, pvalue, evalue = [],[],[]
		for c in keyc:
			try:
				x0, x0err = fx(c)
				if errbar:
				#	x0, x0err = fx(c)
					evalue.append(x0err)
				#else:
				#	x0 = fx(c)
			except ValueError as inst:
				# in the case no value is properly output here
				print inst.args
				if inst.args[0] is not 0:
					# admissible "no value" has error code 0
					raise
			else:
				pvalue.append(x0)
				daynum = (c.datetag- radiation_date).days
				if len(days)>0 and days[-1] >= daynum:
					daynum = days[-1]+.3
				days.append(daynum)
		if avging:
			avgp = np.average(np.array(pvalue))
			pvalue = [x - avgp for x in pvalue]
		if errbar:
			return [days, pvalue, evalue]
		else:
			return [days, pvalue]

	@staticmethod
	def steplocQuad(c, step = 1.5, sample = 8):
		""" quardratic fit for absorption step """
		avgc, errc = c.avgcurve(), c.errcurve()
		index = np.argmax(avgc>step)
		s = slice(index-(sample/2), index+(sample/2)) # take data points: default 2 points before and after
		x1 = x[s]
		A = np.vstack([x1**2, x1, np.ones(len(x1))]).T
		sol = np.linalg.lstsq(A, avgc[s])
		a, b, c = sol[0]
		R=sol[1][0]
		x0 = (-b-np.sqrt(b**2-4*a*(c-step)))/2/a
		x0err = -np.sqrt(R/sample+np.average(errc[s])**2)/(2*a*x0+b)
		return x0 , x0err

	@staticmethod
	def steplocTrsmQuad(c, **kwarg):
		""" quardratic fit for transmission """
		avgc, errc = c.avgtcurve(), c.errtcurve()
		return Curve_TimeFit.steplocTrsmQuadhelper(avgc, errc, **kwarg)

	@staticmethod
	def steplocTrsmQuadMem(c, sidenum, avging = False, **kwarg):
		""" quardratic fit for transmittance step: side members"""
		# avging: subtracting the value from average
		# uses fitting error as error bar
		memc, errc = c.viewt(sidenum), np.zeros(Curve_TimeFit.x.size)
		if memc is 0:
			raise ValueError(0,c.label()+'side '+' abcd'[sidenum]+' is empty')
		if avging:
			xavg=0
			samplenum = 4
			for i in range(1,5):
				try:
					xavg+=steplocTrsmQuadMem(c, i, verbose=False)[0]
				except ValueError:
					samplenum-=1
			xavg /= samplenum
			x0, x0err = Curve_TimeFit.steplocTrsmQuadhelper(memc, errc, **kwarg)
			return (x0-xavg), x0err
		return Curve_TimeFit.steplocTrsmQuadhelper(memc, errc, **kwarg)

	@staticmethod
	def steplocTrsmQuadhelper(curve, errc, step = .7, sample = 8, Lmbd = 0,
										 verbose = True, poslope = True, start = 0):
		index = np.argmin(curve[start:]<step) + start
		if poslope:
			index = np.argmax(curve[start:]<step) + start
		# take data points: default 2 points before and after
		s = slice(index-(sample/2), index+(sample/2))
		x1 = Curve_TimeFit.x[s]
		A = np.vstack([x1**2, x1, np.ones(len(x1))]).T
		sol = np.linalg.lstsq(A, curve[s])
		a, b, c = sol[0]
		R=sol[1][0]
		if poslope:
			x0 = (-b+np.sqrt(b**2-4*a*(c-step)))/2/a + Lmbd
		else:
			x0 = (-b-np.sqrt(b**2-4*a*(c-step)))/2/a + Lmbd		
		x0err = np.sqrt(R/sample+(np.average(errc[s]))**2)/(2*a*x0+b)
		if verbose:
			print '%.2f %.3f error: %.4f %.4f' %(x0, x0err, np.sqrt(R/sample), np.average(errc[s]))
		#pyt.plot(x1, avgc[s],'o')
		#pyt.plot(x1, a*x1**2+b*x1+c)
		#pyt.grid(True)
		#pyt.show()
		return x0 , x0err

	@staticmethod
	def steplocTrsmQuadMem2(c, step = .5, sample = 4):
		""" quadratic fit for transmission; plotting separately for each member (side) curves """
		# same as above but with member curves
		x0 = [0,0,0,0]
		for i in range(1,5):
			ci = c.data[i]
			if ci is not 0:
				cit = Curve.trsm(ci)
				try:
					index = np.argmax(cit<step)
					s = slice(index-(sample/2), index+(sample/2))
					x1 = Curve_TimeFit.x[s]
					A = np.vstack([x1**2, x1, np.ones(len(x1))]).T
					a, b, c0  = np.linalg.lstsq(A, cit[s])[0]
					x0[i-1] = (-b+np.sqrt(b**2-4*a*(c0-step)))/2/a
	#				x0.append((-b+np.sqrt(b**2-4*a*(c-step)))/2/a)
				except ValueError:
					print s,x1, c.label()
					raise
		return x0, 0

	@staticmethod
	def timefit(days, pvalue, evalue, throwlast = None, fx = np.sqrt):
		""" linear fit of functions """
		d = np.array(days[:throwlast])
		p = np.array(pvalue[:throwlast])
		x0 = d[d>=0]
		y = p[d>=0]
		A = np.vstack([fx(x0), x0, np.ones(len(x0))]).T
		sol = np.linalg.lstsq(A, y)
		a, b, c = sol[0]
		R=sol[1][0]
		print a, b, c
		pyt.errorbar(days,pvalue,evalue,fmt = 'r+')
		pyt.plot(x0,a*np.sqrt(x0)+b*x0+c,'--',linewidth=1.5)
		pyt.grid(True)
		pyt.show()
		return

	@staticmethod
	def timefitPara(days, pvalue, evalue, fx ,throwlast = None):
		""" fit parametric functions """
		d = np.array(days[:throwlast])
		p = np.array(pvalue[:throwlast])
		x = d[d>=0]
		y = p[d>=0]
		popt, pcov = curve_fit(fx, x, y)
		print popt
		pyt.errorbar(days,pvalue,evalue,fmt = 'r+')
		pyt.plot(x,fx(x,*popt),'--',linewidth=1.5)
		pyt.grid(True)
		pyt.show()
		return

	@staticmethod
	def normalize(c, s, xlen = 400):
		intgl, xsum= 0, 0
		xnum = s.indices(xlen)[1]-s.indices(xlen)[0] # length of input curve = 400nm
		for i in range(1,5):
			if c.data[i] is not 0:
				intgl += c.data[i][s].sum()
				xsum += xnum
		cnew = c.clone()
		for i in range(1,5):
			if cnew.data[i] is not 0:
				cnew.data[i]*=xsum/intgl
		return cnew

	@staticmethod
	def normalize2(c, s, xlen = 400,factor=1.):
		# individual sides are normalized seperately
		xnum = s.indices(xlen)[1]-s.indices(xlen)[0] # length of input curve = 400nm
		cnew = c.clone()
		for i in range(1,5):
			if c.data[i] is not 0:
				intgl = c.data[i][s].sum()
				cnew.data[i]*=xnum/intgl*factor
		return cnew


