from numpy import binary_repr

input_width_x = 8
input_width_y = 8
inputs_x = [1,-1]
inputs_y = [-1,-1]

n = len(inputs_x)
if n!=len(inputs_y):
	print("Unequal number of inputs. Exiting")

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
dt = 200  # rise & fall time
dt_clk = 100 # rise & fall time for clock
Tsim = 2*T0 + n*T

incpath = "/home/vasid/.git/courses/dic_proj/22nm_HP.pm"
header=".include \"%s\"\n.params Vdd=%f\nvdd vdd gnd dc {Vdd}\nvclk clk gnd PULSE(0 {Vdd} %dp %dp %dp %dp %dp)\n\n"%(incpath,Vdd,T0+T//2,dt_clk,dt_clk,T//2,T)

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
for num in range(n):
	for i in range(input_width_x+input_width_y):
		meascode += ".meas tran val_%d_z%d find V(z%d) at=%dpn\n"%(num,i,i,t+T-dt)
	meascode += "\n"
	
	t += T

footer=".tran 0 %dp UIC\n"%(Tsim)

print(header+"\n"+pwlcode+"\n"+meascode+"\n"+footer)
