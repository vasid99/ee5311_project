from collections import defaultdict
from numpy import binary_repr
from sys import argv

num_inputs = int(argv[1])

# Input space exploration
statebinout = []
changebinout = []
stateout = []
changeout = []
spiceout = []

for i in range(num_inputs):
	stateout.append([])
	changeout.append([])
	spiceout.append("")

visitedtable = defaultdict(list)
for i in range(2**num_inputs):
	for j in range(2**num_inputs):
		visitedtable[i].append(False)

state = 0
change = 0

statebin = binary_repr(state,num_inputs)
changebin = binary_repr(change,num_inputs)
#print(statebin)
statebinout.append(statebin)
changebinout.append(changebin)
for i in range(num_inputs):
	stateout[i].append(int(statebin[-i-1]))
	changeout[i].append(int(changebin[-i-1]))

visitedctr = 0

while visitedctr < 2**num_inputs:
	change = 1
	while change < 2**num_inputs:
		if visitedtable[state][change]==False:
			visitedtable[state][change] = True
			break
		change += 1
	
	if change==2**num_inputs:
		change = state ^ (state + 1)%(2**num_inputs)
		state = (state + 1)%(2**num_inputs)
		visitedctr += 1
	else:
		state = state^change
		visitedctr = 0
	
	statebin = binary_repr(state,num_inputs)
	changebin = binary_repr(change,num_inputs)
	#print(statebin)
	statebinout.append(statebin)
	changebinout.append(changebin)
	for i in range(num_inputs):
		stateout[i].append(int(statebin[-i-1]))
		changeout[i].append(int(changebin[-i-1]))

# SPICE PWL wrapper
# all times in picoseconds
T0 = 1000 # time at PWL initiation
T  = 5000 # time per combination
dt = 200  # rise & fall time
Tsim = 2*T0 + len(stateout[0])*T
dvtol = 0.01
t = T0
incpath = "/home/vasid/.git/courses/dic_proj/22nm_HP.pm"
innames = ['Ci_in','A_in','B_in'] # statebin - LSB to MSB
critoutname = 'S_bar_out'

header=".include \"%s\"\n.params Vdd=1\nvdd vdd gnd dc {Vdd}\n\n"%(incpath)

pwlcode = ""
meascode = ""
for i in range(num_inputs):
	t = T0
	pwlcode += "Vin%d %s gnd PWL(%dp 0 "%(i,innames[i],T0)
	for j in range(len(stateout[i])):
		pwlcode += "%dp {%d*Vdd} %dp {%d*Vdd} "%(t+dt,stateout[i][j],t+T,stateout[i][j])
		t+=T
	pwlcode += ")\n\n"

# .meas code
t = T0 + T
critval_old = ~(stateout[0][0] ^ stateout[1][0] ^ stateout[2][0])
for i in range(1,len(stateout[0])):
	critval = ~(stateout[0][i] ^ stateout[1][i] ^ stateout[2][i])
	
	if critval==critval_old:
		critoutVsense = dvtol if critval==0 else (1-dvtol)
		critoutCross  = 2
	else:
		critoutVsense = 0.5
		critoutCross  = 1
	
	meascode += ".meas tran delay_%d trig V(%s)={%f*Vdd} td=%dp cross=%d targ V(%s)={%f*Vdd} td=%dp cross=%d\n"%(i,innames[-changebinout[i].index('1')-1],0.5,t,1,critoutname,\
	critoutVsense,t,critoutCross)
	critval_old = critval
	t+=T
print(t+T0)
footer="\n.tran 0 %dp UIC\n"%(Tsim)

f = open(argv[2],"w")
f.write(header+pwlcode+meascode+footer)
f.close()	
