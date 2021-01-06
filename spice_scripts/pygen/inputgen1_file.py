from sys import argv
from numpy import binary_repr

try:
	x=int(argv[1])
	y=int(argv[2])
	script_out=open(argv[3],"w")
except:
	print("Usage: python inputgen1_file.py x y outfile")
	exit()

incpath="~/.git/dic_proj/22nm_HP.pm"
xbin=binary_repr(x) if x>=0 else binary_repr(256+x)
ybin=binary_repr(y) if y>=0 else binary_repr(256+y)

script_out.write(".include \"%s\"\n.params Vdd=1 n=0.011U nand=1 a=nand c=3 s=2 inv=4\nvdd vdd gnd dc {Vdd}\n\n"%(incpath))

for i in range(8):
	try:
		script_out.write("vx%d x%d gnd dc %s\n"%(i,i,"{Vdd}" if xbin[-i-1]=="1" else "0"))
	except:
		script_out.write("vx%d x%d gnd dc %s\n"%(i,i,"0"))

script_out.write("\n")

for i in range(8):
	try:
		script_out.write("vy%d y%d gnd dc %s\n"%(i,i,"{Vdd}" if ybin[-i-1]=="1" else "0"))
	except:
		script_out.write("vy%d y%d gnd dc %s\n"%(i,i,"0"))

script_out.write("\n")

for i in range(16):
	script_out.write(".meas tran val_z%d find V(z%d) at=1.9n\n"%(i,i))

script_out.write("\n")

script_out.write(".tran 0 2n UIC\n")
script_out.close()
