##
##
##   	Cold/ warm sample
##
##		Created: Jul 25 2016
##
##

allcurves = readCurveFile('measuredates_July_stability.py', verbose = 1, skips = 1)
refcurves = allcurves
farbGruppe = [['blue', 'darkblue','darkslateblue','royalblue', 'steelblue','darkcyan'],
			['red', 'darkred', 'crimson', 'orangered','salmon'],
			['green', 'darkgreen', 'olive', 'darkturquoise', 'greenyellow','sage'],
			['magenta','blueviolet','purple','darkmagenta','darkviolet'], 
			['slategray', 'dimgrey']]
farben  = ['blue'] + farbGruppe[2]
farben2 = farbGruppe[1]
cLineStyle = ['dashed'] + ['solid']*3
cLabel = ['Ref. EJ200-1X-3',r'23$^\circ$C',r'-30$^\circ$C']
## Parameters 
keyword = 'EJ200-1X-10'			# read sample
keyword2 = 'EJ200-1X-11'						# read sample
refkeyword = 'EJ200-1X-3'				# reference sample
s = Curve.makeslice(300,600)			 		# x-range (band of wavelength in nm)
baseline = False 			# set to show baseline curve -- Overrides other settings
t = True					# transmission or absorption curve; None for absorption
df = True					# difference instead of ratio plot (for absorption curve)
isDiff = False 					# overrides df: show
showRef = True
showErr = True 			# Show cyan Error x10 curve
refnum = -1 					# number of reference (from 0)
shr = dict(height_ratios = [3,2])		#subplot height ratio
figsize = (10,10)
newdate = False
isFirstLast = False 		# choose only first or last curve
legFont = 14				# legend font size
isBlocked = False			# Blocks interaction: if false the program should be run
							# with the tag "-i"
isFarben = True
isOrigLabel = False			# choose to print original label
isOrigLinestyle = False		# default linestyle
tLabel = 'Transmission' if t else 'Absorption'
titleGen = r"'EJ200-1X Cold Sample '+tLabel+' Spectrum'"
ratioyrange=None

dateN2 = date(2015,12,19)
dateN3 = date(2016,01,14)
dateN4 = date(2016,01,11)
if newdate:
	dateN4 = date(2016,03,25)
dateCT = date(2015,11,3) # inaccurate


allc = [sum(curvesKeyword(allcurves, name = keyword)[1:])]
allcurves = allc + [sum(curvesKeyword(allcurves, name = keyword2)[1:])]
refcurves = [sum(curvesKeyword(refcurves, name = refkeyword))]



#def lbl_gen(c):
#	# local shorthand: Can Edit
#	return c.label(hasDay=False)