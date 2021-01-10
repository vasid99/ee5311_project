from numpy import binary_repr

input_width = 8
inputs_x = [1,2,-1]
inputs_y = [1,4,-1]

n = len(inputs_x)
if n!=len(inputs_y):
	print("Unequal number of inputs. Exiting")

inputs_x_bin = []
inputs_y_bin = []

for i in range(n):
	inputs_x_bin.append(binary_repr(\
	inputs_x[i] if inputs_x[i]<=(2**(input_width-1)-1) else (2**input_width+inputs_x[i])\
	,input_width))
	
	inputs_y_bin.append(binary_repr(\
	inputs_y[i] if inputs_y[i]<=(2**(input_width-1)-1) else (2**input_width+inputs_y[i])\
	,input_width))

# all times in picoseconds
T0 = 1000 # time at PWL initiation
T  = 5000 # time per combination
dt = 200  # rise & fall time
Tsim = 2*T0 + n*T

incpath = "/home/vasid/.git/courses/dic_proj/22nm_HP.pm"
header=".include \"%s\"\n.params Vdd=1\nvdd vdd gnd dc {Vdd}\n\n"%(incpath)
pwlcode = ""
footer="\n.tran 0 %dp UIC\n"%(Tsim)

for i in range(input_width):
	t = T0
	pwlcode += "Vx%d x%d gnd PWL(%dp 0 "%(i,i,T0)
	for j in range(n):
		pwlcode += "%dp {%s*Vdd} %dp {%s*Vdd} "%(t+dt,inputs_x_bin[j][-i-1],t+T,inputs_x_bin[j][-i-1])
		t+=T
	pwlcode += ")\n"

pwlcode += "\n"

for i in range(input_width):
	t = T0
	pwlcode += "Vy%d y%d gnd PWL(%dp 0 "%(i,i,T0)
	for j in range(n):
		pwlcode += "%dp {%s*Vdd} %dp {%s*Vdd} "%(t+dt,inputs_y_bin[j][-i-1],t+T,inputs_y_bin[j][-i-1])
		t+=T
	pwlcode += ")\n"

print(header+pwlcode+footer)
