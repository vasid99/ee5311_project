from numpy import binary_repr
from sys import argv

input_width_x = 8
input_width_y = 8
inputs_x = [0,1,-1,-1]
inputs_y = [0,-1,-1,1]

n = len(inputs_x)
if n!=len(inputs_y):
	print("Unequal number of inputs. Exiting")

usage = "Usage:\n1. python gen_fn.py test     [outfile]\n2. python gen_fn.py debug    [outfile]\n3. python gen_fn.py delaychk [outfile]"
try:
	if argv[1]=='test':
		dbg  = False
		dchk = False
	elif argv[1]=='debug':
		dbg  = True
		dchk = False
	elif argv[1]=='delaychk':
		dbg  = False
		dchk = True
	else:
		print(usage)
		exit()
except:
	print(usage)
	exit()

try:
	outfile = argv[2]
except:
	outfile = ""

inputs_x_bin = []
inputs_y_bin = []

for i in range(n):
	inputs_x_bin.append(binary_repr(\
	inputs_x[i] if inputs_x[i]<=(2**(input_width_x-1)-1) else (2**input_width_x+inputs_x[i])\
	,input_width_x))
	
	inputs_y_bin.append(binary_repr(\
	inputs_y[i] if inputs_y[i]<=(2**(input_width_y-1)-1) else (2**input_width_y+inputs_y[i])\
	,input_width_y))

# all times in picoseconds
Vdd = 1
T0 = 1000 # time at PWL initiation
T  = 5000 # time per combination
T0_clk = T0 + T//2 # time at PWL initiation for clock
dt = 200  # rise & fall time
dt_clk = 100 # rise & fall time for clock
Tsim = 2*T0 + n*T

incpath = "../22nm_HP.pm"
header=".include \"%s\"\n.params Vdd=%f\nvdd vdd gnd dc {Vdd}\nvclk clk gnd PULSE(0 {Vdd} %dp %dp %dp %dp %dp)\n"%(incpath,Vdd,T0_clk,dt_clk,dt_clk,T//2,T)

pwlcode = ""

for i in range(input_width_x):
	t = T0
	pwlcode += "Vx%d x%d gnd PWL(%dp 0 "%(i,i,T0)
	for j in range(n):
		pwlcode += "%dp {%s*Vdd} %dp {%s*Vdd} "%(t+dt,inputs_x_bin[j][-i-1],t+T,inputs_x_bin[j][-i-1])
		t+=T
	pwlcode += ")\n"

pwlcode += "\n"

for i in range(input_width_y):
	t = T0
	pwlcode += "Vy%d y%d gnd PWL(%dp 0 "%(i,i,T0)
	for j in range(n):
		pwlcode += "%dp {%s*Vdd} %dp {%s*Vdd} "%(t+dt,inputs_y_bin[j][-i-1],t+T,inputs_y_bin[j][-i-1])
		t+=T
	pwlcode += ")\n"

meascode = ""
t = T0
tclk = T0_clk
for num in range(n):
	if dbg:
		for i in range(input_width_x*input_width_y):
			i1=i//8
			i2=i%8
			meascode += ".meas tran val_%d_FA_Co_bar_%d_%d find V(FA_Co_bar_%d_%d) at=%dp\n"%(num,i1,i2,i1,i2,t+T-dt)
		meascode += "\n"
	
		for i in range(input_width_x*input_width_y):
			i1=i//8
			i2=i%8
			meascode += ".meas tran val_%d_FA_S_bar_%d_%d find V(FA_S_bar_%d_%d) at=%dp\n"%(num,i1,i2,i1,i2,t+T-dt)
		meascode += "\n"	
	
	for i in range(input_width_x+input_width_y):
		meascode += ".meas tran val_%d_z%d find V(z%d) at=%dp\n"%(num,i,i,t+T-dt)
	
	if dchk:
		meascode += "\n.meas tran delay_%d_clk_7_7 trig V(clk) = {0.5*Vdd} td = %dp cross = 1 targ V(FA_S_bar_7_7) = {0.5*Vdd} td = %dp cross = 1\n.meas tran delay_%d_clk_6_1 trig V(clk) = {0.5*Vdd} td = %dp cross = 1 targ V(FA_S_bar_6_1) = {0.5*Vdd} td = %dp cross = 1\n\n"%(num,tclk,tclk,num,tclk,tclk)
	
	t += T
	tclk += T

footer=".tran 0 %dp UIC\n"%(Tsim)

outcode=header+"\n"+pwlcode+"\n"+meascode+"\n"+footer
if outfile:
	f = open(outfile,"w")
	f.write(outcode)
	f.close()
else:
	print(outcode)
