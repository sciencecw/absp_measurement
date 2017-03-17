import numpy as np
import matplotlib.pyplot as pyt
from datetime import date
import sys

## readCurveSequence.py
## Created: 05Apr2016

## Read from Text file a list of csv filenames
## read csv files and plot all curves in sequence
## (Filters available)

from Curve import (Curve, curvesKeyword, curveCreation, 
					specPlotter,curvesAge, curvesRef, readCurveFile)

x= np.linspace(600,200,401)


print sys.argv 

if len(sys.argv)>1:
	allcurves = curveCreation(date.today(),sys.argv[1:2],skips=3)
else:
	#allcurves = curveCreation(date(2016,10,5), 		['data/EJ_20161005_air_all.csv'], verbose = 1,skips=1)
	#allcurves = curveCreation(date(2016,10,11), 	['data/EJ_20161011_air.csv'], verbose = 1,skips=1)
	allcurves = curveCreation(date(2016,11,1), ['data/EJ_20161101_air_calib.csv','data/EJ_20161101_air_calib2.csv', 'data/EJ_20161101_air.csv'], verbose = 1,skips=1)
	#
	#allcurves = readCurveFile('measuredates_Oct.txt', verbose = 1, skips = 1)


farben = ['blue', 'green', 'darkcyan','red' ,'magenta','blueviolet', 'slategray','magenta']
farben += ['hotpink', 'salmon','springgreen','chocolate', 'crimson']

## parameters 
mode = 2 		
# 0: plot average 1: plot all member curves
# 2: all memeber curves with comparison
# 3: all memeber curves with Diff
keyword = '' #'EJ200SP-1P-N1' #'1X1P N1'						# read sample
#keyword2 = '1X1P N6'						# read sample
s = Curve.makeslice(300,600)		# x-range (band of wavelength in nm)
t = True					# transmission or absorption curve; None for absorption
newdate = True


dateN2 = date(2015,12,19)
dateN3 = date(2016,01,14)
dateN4 = date(2016,01,11)
if newdate:
	dateN4 = date(2016,03,25)
dateCT = date(2015,11,3) # inaccurate

allc = curvesKeyword(allcurves, name = keyword) 
#allc2 = curvesKeyword(allcurves, name = keyword2)
#allc += allc2
#allc = curveCreation(date.today(), ['data/EJ_20160328_air_SPN4.csv'], verbose = 1)


print 'Drawing curves ...\n'
for c in allc:
	[c.plot,c.plotallcurves,c.plotallcurvesComp,c.plotallcurvesDiff][mode](t=t,
		ratioyrange=[-0.06,0.06],save = False, plotting = True, s = s)




