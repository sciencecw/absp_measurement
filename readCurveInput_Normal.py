##
##
##   	Ordinary sample comparison
##
##		Created: Aug 1st 2016
##
##

allcurves = readCurveFile('measuredates_Oct.txt', verbose = 1, skips = 1)
#allcurves = curveCreation(date(2016,10,10), 
#		['data/EJ_20161010_avikak2.csv'], verbose = 1,skips=2)
refcurves = allcurves
farbGruppe = [['blue', 'darkblue','darkslateblue','royalblue', 'steelblue','darkcyan'],
			['red', 'darkred', 'crimson', 'orangered','salmon'],
			['green', 'darkgreen', 'olive', 'darkturquoise', 'greenyellow','sage'],
			['magenta','blueviolet','purple','darkmagenta','darkviolet'], 
			['slategray', 'dimgrey']]
farben  = ['blue'] + farbGruppe[2] + ['gray']*10
farben2 = farbGruppe[1]+ ['gray']*10
cLineStyle = ['dashed'] + ['solid']*40
#cLabel = ['Ref. EJ200-1X-3',r'23$^\circ$C',r'-30$^\circ$C']
## Parameters 
keyword = 'EJ260-1X1P-N1'			# read sample
keyword2 = 'xxx'			# read sample
refkeyword = 'EJ260-1X1P-N1'				# reference sample
s = Curve.makeslice(350,600)			 		# x-range (band of wavelength in nm)
baseline = False 			# set to show baseline curve -- Overrides other settings
t = True					# transmission or absorption curve; None for absorption
df = True					# difference instead of ratio plot (for absorption curve)
isDiff = False 					# overrides df: show
showRef = True
showErr = True 			# Show cyan Error x10 curve
refnum = -1 					# number of reference (from 0)
shr = dict(height_ratios = [3,2])		#subplot height ratio
figsize = (13,10)
newdate = False
isFirstLast = False 		# choose only first or last curve
legFont = 10				# legend font size
isBlocked = False			# Blocks interaction: if false the program should be run
							# with the tag "-i"
isFarben = True
isOrigLabel = True			# choose to print original label
isOrigLinestyle = False		# default linestyle
ratioyrange= [-.15,.05]
