from sys import argv
from numpy import binary_repr

try:
	x=int(argv[1])
	y=int(argv[2])
except:
	print("Usage: python inputgen1_print.py x y")
	exit()

incpath="PUT MODEL FILE PATH HERE"
xbin=binary_repr(x) if x>=0 else binary_repr(256+x)
ybin=binary_repr(y) if y>=0 else binary_repr(256+y)

print(".include \"%s\"\n.params Vdd=1 n=0.011U nand=1 a=nand c=3 s=2 inv=4\nvdd vdd gnd dc {Vdd}\n"%(incpath))

for i in range(8):
	try:
		print("vx%d x%d gnd dc %s\n"%(i,i,"{Vdd}" if xbin[-i-1]=="1" else "0"),end="")
	except:
		print("vx%d x%d gnd dc %s\n"%(i,i,"0"),end="")

print("")

for i in range(8):
	try:
		print("vy%d y%d gnd dc %s\n"%(i,i,"{Vdd}" if ybin[-i-1]=="1" else "0"),end="")
	except:
		print("vy%d y%d gnd dc %s\n"%(i,i,"0"),end="")

print("")

for i in range(16):
	print(".meas tran val_z%d find V(z%d) at=1.9n\n"%(i,i),end="")

print("\n.tran 0 2n UIC")
