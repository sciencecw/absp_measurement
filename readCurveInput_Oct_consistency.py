### 
###  Check consistency of measurements by Avi and Kak
### 

side = 1
print "side : ", side

## Curves to be read
allctemp = curveCreation(date(2016,10,14), 
		['data/EJ_20161014_ameerruhikak.csv'], verbose = 1,skips=2, sepcurve=True)

#allctemp = curveCreation(date(2016,10,13), 
#		['data/EJ_20161013_kakandres.csv', 'data/EJ_20161013_kak_air.csv'], verbose = 1,skips=2)#, sepcurve=True)
#allctemp2 = curveCreation(date(2016,10,10), 
#		['data/EJ_20161010_avikak2.csv'], verbose = 1,skips=2)#, sepcurve=True)
#allctemp = [c for c in allctemp if c.view(side, t=True) is not 0]
#allctemp2 = [c for c in allcurves2 if c.view(side, t=True) is not 0]
keyword = 'EJ200SP-1P-N1'						# read sample
#allcurves = curvesKeyword(allctemp, name =  keyword ) 
#print 'kak entries: ', len(allcurves)
allcurves = curvesKeyword(allctemp, name =  keyword + ' Kak')
allcurves += curvesKeyword(allctemp, name = keyword + ' Ruhi')
#allcurves += curvesKeyword(allctemp, name = keyword + ' Ruhi')



data_cref = Curve.absp(sum([c.view(side, t=True) for c in allcurves])/len(allcurves))
#data_cref = Curve.absp(sum([c.avgtcurve() for c in allcurves])/len(allcurves))
refcurves = [Curve(keyword, date.today())] # averaging with showing a side
refcurves[0].add(side, data_cref)			   # ! Brute Force
#refcurves[0].add(1, data_cref)			   # ! Brute Force
#refcurves = allcurves
titleGen = r"refkeyword+' '+tLabel +' Spectrum Side ' + ' ABCD'[side]"

if False:
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

farben = ['lightgray']+['gray']*5 
farben += ['blue', 'darkblue','darkslateblue','royalblue', 'darkblue','royalblue', 'darkblue']
farben +=  ['red','darkred', 'crimson', 'orangered','salmon'] 
#farben += ['gray']*3+['red','magenta','blueviolet']
#farben += ['gray']*2+['blue', 'darkblue','darkslateblue'] + ['gray']*20

## Parameters 
keyword2 = 'xxxx'						# read sample
refkeyword = keyword 					# reference sample
s = Curve.makeslice(300,600) 			# x-range (band of wavelength in nm)
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
#isBlocked = True			# Blocks interaction: if false the program should be run
							# with the tag "-i"
isOrigLabel = True			# choose to print original label
lwidth = 1. 					# default line width


#cLabel = [None]* 3 +['07/12', '07/13'] +[None]*3 +['07/18']*3 +  [None]*2 + ['07/20']*3  + [None]*2  

tLabel = 'Transmission' if t else 'Absorption'
ratioyrange=[-0.04,0.04]

def lbl_gen(c):
	# local shorthand: Can Edit
	return c.label(nslice = slice(0,-1),  #dslice = slice(0,0)
		     ) if isOrigLabel else itercLabel.next()
