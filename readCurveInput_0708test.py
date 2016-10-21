
allcurves = curveCreation(date(2016,7,8),['data/EJ_20160708_air_test.csv'],
							verbose = 1, skips = 3,sepcurve=True)
			# separate curves are inputed

## selects only EJ260-1X1P... also only the a side measurements
allcurves = curvesKeyword(allcurves, name =  'EJ260-1X1P') [:27]
allcurves = [c for c in allcurves if c.view(1) is not 0]
refcurves = [sum(allcurves[4:15])] 
farbGruppe = [['blue', 'darkblue','darkslateblue','royalblue', 'steelblue','darkcyan'],
			['red', 'darkred', 'crimson', 'orangered','salmon'],
			['green', 'darkgreen', 'olive', 'darkturquoise', 'greenyellow','sage'],
			['magenta','blueviolet','purple','darkmagenta','darkviolet'], 
			['slategray', 'dimgrey']]



farben = [None]+ ['darkgray']*11+farbGruppe[0][:5]+farbGruppe[1][:2]+farbGruppe[3][:5]
#farben += farbGruppe[1][:4] + ['dimgrey'] + farbGruppe[2][:2] + farbGruppe[3]
farben2 = ['crimson','darkcyan','green','darkgreen']
#cLabel = ['Stationary'] + [None]*4 + ['Switiching Samples'] + [None]*4 + ['Stationary'] + [None]*10
cLabel = ['Initial measurement'] #['Side '+'ABCD'[i] for i in range(1)]
cLabel+=['Stationary'] + [None]*10
cLabel+=['Replaced by Vineet']*3+[None]*2 + ['Replaced by Kak']*2 + ['recalibrated'] + ['Replaced by Kak']*2 + [None]*5
#cLabel += ['Fixed by Vineet','Fixed by Kak','Unmoved','Push to a side']
cLineStyle = ['dashed']*1  + ['solid']*16+[':']*2+ ['solid']*5

## Parameters 
keyword = ' '									# read sample
keyword2 = '###########'						# read sample
refkeyword = keyword 							# reference sample
s = Curve.makeslice(350,600) 	##x-range (band of wavelength in nm)
#s = slice(None) 
baseline = False 			# set to show baseline curve -- Overrides other settings
t = True					# transmission or absorption curve; None for absorption
df = False					# difference instead of ratio plot (for absorption curve)
showRef = False
showErr = False 			# Show cyan Error x10 curve
refnum = 0 					# number of reference (from 0)
shr = dict(height_ratios = [3,2])		#subplot height ratio
figsize = (10,10)
newdate = False
isFirstLast = False 		# choose only first or last curve
legFont = 10				# legend font size
isBlocked = False			# Blocks interaction: if false the program should be run
							# with the tag "-i"
isOrigLabel = False			# choose to print original label
isOrigLinestyle = False		# default linestyle


tLabel = 'Transmission' 	#if t else 'Absorption'
titleGen = r" 'EJ260-1X1P-N1 Transmission Spectrum July08 Test' "
ratioyrange=[-0.06,0.06]


if False:
	refkeyword = keyword = sys.argv[1]			# input mode
	if len(sys.argv) > 2:
		refkeyword = sys.argv[2]

