from numpy import binary_repr
from sys import argv

try:
	x=int(argv[1])
	y=int(argv[2])
except:
	print("Usage: python measgen.py x y [outfile]")
	exit()

xbin=binary_repr(x) if x>=0 else binary_repr(256+x)
ybin=binary_repr(y) if y>=0 else binary_repr(256+y)

Vdd = 1
tsim  = 2000
tmeas = 1900
pm_file_path="/home/vasid/.git/courses/dic_proj/22nm_HP.pm"

finalcode = ""

finalcode += ".include \"%s\"\n.params Vdd=%f n=0.011U nand=1 a=nand c=3 s=2 inv=4\nvdd vdd gnd dc {Vdd}\n\n"%(pm_file_path,Vdd)

for i in range(8):
	try:
		finalcode += "vx%d x%d gnd dc %s\n"%(i,i,"{Vdd}" if xbin[-i-1]=="1" else "0")
	except:
		finalcode += "vx%d x%d gnd dc %s\n"%(i,i,"0")

finalcode += "\n"

for i in range(8):
	try:
		finalcode += "vy%d y%d gnd dc %s\n"%(i,i,"{Vdd}" if ybin[-i-1]=="1" else "0")
	except:
		finalcode += "vy%d y%d gnd dc %s\n"%(i,i,"0")

finalcode += "\n"

for i in range(64):
	i1=i//8
	i2=i%8
	finalcode += ".meas tran val_FA_Co_bar_%d_%d find V(FA_Co_bar_%d_%d) at=%dp\n"%(i1,i2,i1,i2,tmeas)

finalcode += "\n"

for i in range(64):
	i1=i//8
	i2=i%8
	finalcode += ".meas tran val_FA_S_bar_%d_%d find V(FA_S_bar_%d_%d) at=%dp\n"%(i1,i2,i1,i2,tmeas)

finalcode += "\n"	

for i in range(16):
	finalcode += ".meas tran val_z%d find V(z%d) at=%dpn\n"%(i,i,tmeas)

finalcode += "\n.tran 0 %dp UIC"%(tsim)

outcode = finalcode
try:
	f = open(argv[3],"w")
	f.write(outcode)
	f.close()
except:
	print(outcode)
