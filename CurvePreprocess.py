import sys
import os.path

filename = sys.argv[1]
for filename in sys.argv[1:]:
	dn, bn = os.path.split(filename)
	print dn,'>><<', bn
	f = open(filename)
	wf = open(dn+'/../data/'+ bn,'w')
	line = f.readline()
	wf.write(line.rstrip(',\r\n') + ',\r\n')
	while True:
		line = f.readline()
		if not line.rstrip(',\r\n'):
			break
		wf.write(line.rstrip(',\r\n') + '\r\n')
	f.close()
	wf.close()
