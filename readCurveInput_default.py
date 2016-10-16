##
##
##   	Default setting
##		change the file with care
##
##		Created: Jul 08 2016
##
##

x= np.linspace(600,200,401)
farben= ['blue', 'green', 'red', 'magenta', 'cyan'] ## default color
farben += ['hotpink', 'salmon','slategray','springgreen','chocolate', 'crimson']
farben2 = []

## Parameters 
keyword = 'EJ260-1X1P-N1'			# read sample
keyword2 = 'xx'						# read sample
refkeyword = keyword				# reference sample
s = slice(None)			 		# x-range (band of wavelength in nm)
baseline = False 			# set to show baseline curve -- Overrides other settings
t = True					# transmission or absorption curve; None for absorption
df = True					# difference instead of ratio plot (for absorption curve)
isDiff = False 					# overrides df: show
showRef = True
showErr = True 			# Show cyan Error x10 curve
refnum = 0 					# number of reference (from 0)
shr = dict(height_ratios = [3,2])		#subplot height ratio
figsize = (10,10)
newdate = False
isFirstLast = False 		# choose only first or last curve
legFont = 10				# legend font size
lwidth = 1 					# default line width
isBlocked = False			# Blocks interaction: if false the program should be run
							# with the tag "-i"
isFarben = True
isOrigLabel = True			# choose to print original label
isOrigLinestyle = True		# default linestyle
tLabel = 'Transmission' if t else 'Absorption'
titleGen = r"refkeyword+' '+tLabel+' Spectrum'"
ratioyrange=None

dateN2 = date(2015,12,19)
dateN3 = date(2016,01,14)
dateN4 = date(2016,01,11)
if newdate:
	dateN4 = date(2016,03,25)
dateCT = date(2015,11,3) # inaccurate

Curve.irrdates = Curve.readIrrDate('irraddates.txt')
def avg_gen(c):
	# local shorthand
	return c.avgcurve(t=t)[s]
def lbl_gen(c):
	# local shorthand: Can Edit
	return c.label() if isOrigLabel else itercLabel.next()
	