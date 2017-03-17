##
##
##      File: readCurveInput_Oct_Normal.py
##   	Ordinary sample comparison
##		Used also for reference comparison
##
##		save() to save figure
##
##		Created: Oct 11th 2016
##
##

allcurves = readCurveFile('measuredates/measuredates_Oct.txt', verbose = 1, skips = 1)
#allcurves = curveCreation(date(2016,10,10), 
#		['data/EJ_20161010_avikak2.csv'], verbose = 1,skips=2)
refcurves = allcurves
farbGruppe = [['blue', 'darkblue','darkslateblue','royalblue', 'steelblue','darkcyan'],
			[ 'darkred', 'crimson','red', 'orangered','salmon'],
			['green', 'darkgreen', 'olive', 'darkturquoise', 'greenyellow','sage'],
			['magenta','blueviolet','purple','darkmagenta','darkviolet'], 
			['slategray', 'dimgrey']]
farben  = ['blue', 'darkblue'] #
farben+=  farbGruppe[1] + ['gray']*5 #['green' ,'red']  +
farben2 = farbGruppe[1]+ ['gray']*10
cLineStyle = ['dashed'] + ['solid']*40
#cLabel = ['Ref. EJ200-1X-3',r'23$^\circ$C',r'-30$^\circ$C']
## Parameters 
basename = 'EJ200PS-1X1P-' #sys.argv[1] #
keyword =  basename +'5'	# read sample
keyword2 = 'xxx'			# read sample
refkeyword = basename+'1'	# keyword # reference sample
s =  Curve.makeslice(350,600)			 		# x-range (band of wavelength in nm)
baseline = False 			# set to show baseline curve -- Overrides other settings
t = True					# transmission or absorption curve; None for absorption
df = False					# difference instead of ratio plot (for absorption curve)
isDiff = False 					# overrides df: show
showRef = True
showErr = True 			# Show cyan Error x10 curve
refnum = 0					# number of reference (from 0)
shr = dict(height_ratios = [3,2])		#subplot height ratio
figsize = (13,10)
newdate = False
isFirstLast = False 		# choose only first or last curve
leg_kwarg['loc'] = 4 		# upperleft = 2 lowerright =4
isBlocked = False			# Blocks interaction: if false the program should be run
							# with the tag "-i"
isFarben = True
isOrigLabel = True			# choose to print original label
isOrigLinestyle = False		# default linestyle
ratioyrange= [-1., 1.]
titleGen = r"keyword+' '+tLabel+' Spectrum'"

fxm = lambda c,i:ctf.steplocTrsmQuadMem(ctf.normalize2(c,Curve.makeslice(490,530)), i, avging = False, step = .4, verbose=True) # taking average



if False:
	def avg_gen(c):
		# local shorthand
		# *** Special: to cancel out effect of higher attenuation on C side for EJ200SP-1P-N1 only***
		nonzero = c.arraynzd()[(0,1,3),:]
		temp = np.average(c.trsm(nonzero),0)[s]
		return temp
if False:
	# brute force averaging of reference curves
	rs = slice(0,5) # reference slicing
	refcurves = curvesKeyword(refcurves, name = refkeyword) 
	data_cref = Curve.absp(sum([avg_gen(c) for c in refcurves[rs]])/len(refcurves[rs]))
	refcurves = [Curve(keyword, date.today())] # averaging with showing a side
	for i in range(4): refcurves[0].add(i, data_cref)			   # ! Brute Force

def save():
	fig.savefig('plots/SpecComp'+keyword+'.pdf')
	#fig2.savefig('plots/SpecComp'+keyword+'_sub.pdf')


def makesubgraph(s1=Curve.makeslice(370,430),size=(3,3)):
	fig2 = pyt.figure(figsize = size)
	for (i,c) in enumerate(allc):
		pyt.plot(x[s1], (avg_gen(c)/ref-1)[s1],linewidth = lwidth,
						color = farben[i+1])
	pyt.show(block = isBlocked)
	return fig2

