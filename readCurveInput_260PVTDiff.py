## aims to show that discrepency in EJ260PVT-1X1P- N6,7 is due to geometrical effects
## if one side is longer than the other, then the "diff" of absoption values should be const

# a' = lnt' = (1+dx/x) lnt
# therefore a'/a is the same as the ratio of sides

## Curves to be read
allcurves = readCurveFile('measuredates_June.txt', verbose = 0, skips = 1)
refcurves = allcurves

farben = [ 'red', 'darkred','green', 'crimson','magenta','darkred','darkmagenta']
farben2 = ['crimson','darkcyan','green','darkgreen']
farben += ['hotpink','green','darkcyan' ,'olive','orangered', 'slategray','magenta']

## Parameters 
keyword = 'EJ260PVT-1X1P-N6'						# read sample
keyword2 = 'EJ260PVT-1X1P-N7'								# read sample
refkeyword = 'EJ260PVT-1X1P-N1' 					# reference sample
if False:
	refkeyword = keyword = sys.argv[1]			# input mode
	if len(sys.argv) > 2:
		refkeyword = sys.argv[2]
s = Curve.makeslice(350,600) 					##x-range (band of wavelength in nm)
#s = slice(None) 
baseline = False 			# set to show baseline curve -- Overrides other settings
t = None					# transmission or absorption curve; None for absorption
df = True					# difference instead of ratio plot (for absorption curve)
isDiff = True 					# overrides df: show
showRef = True
refnum = 0 					# number of reference (from 0)
shr = dict(height_ratios = [3,2])		#subplot height ratio
newdate = False
isFirstLast = True 		# choose only first or last curve
legFont = 12				# legend font size
isBlocked = False			# Blocks interaction: if false the program should be run
							# with the tag "-i"
tLabel = 'Transmission' if t else 'Absorption'
titleGen = r"refkeyword+' '+tLabel+' Spectrum'"
#ratioyrange=[-0.06,0.06]

dateN2 = date(2015,12,19)
dateN3 = date(2016,01,14)
dateN4 = date(2016,01,11)
if newdate:
	dateN4 = date(2016,03,25)
dateCT = date(2015,11,3) # inaccurate


print "260PVTDiff"