
allcurves = curveCreation(date(2016,06,27),['data/EJ_20160627_air_test.csv'],
							verbose = 1, skips = 3,sepcurve=True)
allcurves += curveCreation(date(2016,06,27),['data/EJ_20160627_air_test1.csv'],
							verbose = 1, skips = 3,sepcurve=True,abspmode=False)
allcurves += curveCreation(date(2016,06,27),['data/EJ_20160627_air_test2.csv'],
							verbose = 1, skips = 3,sepcurve=True,abspmode=False)
refcurves = allcurves

farbGruppe = [['blue', 'darkblue','darkslateblue','royalblue', 'steelblue','darkcyan'],
['red', 'darkred', 'crimson', 'orangered','salmon'],
['green', 'darkgreen', 'olive', 'darkturquoise', 'greenyellow','sage'],
['magenta','blueviolet','purple'], 
['slategray', 'dimgrey']]





farben = ['slategray']*5+farbGruppe[0][:5]#+farbGruppe[1][:4]
#farben = [(.2+i/18.,)*3 for i in range(5)]+farbGruppe[0][:7]+farbGruppe[1]
farben += farbGruppe[1][:4] + ['dimgrey'] + farbGruppe[2][:2] + farbGruppe[3]
farben2 = ['crimson','darkcyan','green','darkgreen']
#cLabel = ['Stationary'] + [None]*4 + ['Switiching Samples'] + [None]*4 + ['Stationary'] + [None]*10
cLabel = ['Stationary'] + [None]*4+['Replaced by Vineet']*6 + ['Unmoved']*3
cLabel += ['Fixed by Vineet','Fixed by Kak','Unmoved','Push to a side']

## Parameters 
keyword = 'EJ200SP-1P-N1'						# read sample
keyword2 = 'EJ2ffffffff'						# read sample
refkeyword = keyword #'EJ200' 					# reference sample
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

tLabel = 'Transmission' 	#if t else 'Absorption'
titleGen = r"refkeyword+' '+tLabel+' Spectrum'"
ratioyrange=[-0.06,0.06]


if False:
	refkeyword = keyword = sys.argv[1]			# input mode
	if len(sys.argv) > 2:
		refkeyword = sys.argv[2]

