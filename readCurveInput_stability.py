### 
###  Measure day-to-day Stability of June/ July measurements
###  With old/ new piece holders
### 

## Curves to be read
allcurves = readCurveFile('measuredates_July_stability.py', verbose = 1, skips = 1)
#allcurves = readCurveFile('measuredates_June.txt', verbose = 0, skips = 1)
refcurves = allcurves
keyword = 'EJ260-1X1P-N1'						# read sample
titleGen = r"refkeyword+' '+tLabel+' Spectrum'"
allcurves = curvesKeyword(allcurves, name =  keyword) 
refcurves = [sum(allcurves)] 

if False: # turn to false if not plotting one of the sides
	side = 4
	print "side : ", side
	data_cref = Curve.absp(sum([c.view(side, t=True) for c in allcurves])/len(allcurves))
	refcurves = [Curve(keyword, date.today())] # averaging with showing a side
	refcurves[0].add(side, data_cref)			   # ! Brute Force
	titleGen = r"refkeyword+' '+tLabel+' Spectrum Side ' + ' ABCD'[side]"
	def avg_gen(c):
		# local shorthand
		try:	
			return c.view(side, t=t)[s]
		except TypeError as err:
			print c.datetag
			print c.nametag
			print c.printType()
			print err
			print 
			raise
#fig.savefig('plots/stability_July2016/'+refkeyword+'stability_side'+' ABCD'[side]+ '.pdf')


#isFarben = False
#farben = ['black','green','magenta','darkmagenta']
#farben += ['greenyellow','blue', 'darkblue','red', 'orangered'  ,
#'darkcyan','slategray', 'blue', 'darkblue'] + ['gray']*20

farben = ['blue']+['gray']*3 + ['blue', 'darkblue','darkslateblue','royalblue']
farben += ['gray']*8+ ['green', 'darkgreen'] 
#farben += ['gray']*3+['red','magenta','blueviolet']
#farben += ['gray']*2+['blue', 'darkblue','darkslateblue'] + ['gray']*20

## Parameters 
keyword2 = 'xxxx'						# read sample
refkeyword = keyword 					# reference sample
s = Curve.makeslice(350,600) 			# x-range (band of wavelength in nm)
baseline = False 			# set to show baseline curve -- Overrides other settings
t = True					# transmission or absorption curve; None for absorption
df = True					# difference instead of ratio plot (for absorption curve)
isDiff = False 				# overrides df: show
showRef = True
refnum = 0 					# number of reference (from 0)
shr = dict(height_ratios = [3,2])		#subplot height ratio
figsize = (6,8)				# (W, H)
newdate = False
isFirstLast = False 		# choose only first or last curve
legFont = 10				# legend font size
isBlocked = False			# Blocks interaction: if false the program should be run
							# with the tag "-i"
isOrigLabel = True			# choose to print original label


#cLabel = [None]* 3 +['07/12', '07/13'] +[None]*3 +['07/18']*3 +  [None]*2 + ['07/20']*3  + [None]*2  

tLabel = 'Transmission' if t else 'Absorption'
ratioyrange=[-0.07,0.07]

dateN2 = date(2015,12,19)
dateN3 = date(2016,01,14)
dateN4 = date(2016,01,11)
if newdate:
	dateN4 = date(2016,03,25)
dateCT = date(2015,11,3) # inaccurate

