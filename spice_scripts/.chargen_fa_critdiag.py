from numpy import binary_repr
from sys import argv

# ---SCRIPT PARAMETERS---
# input sequence generator parameters
num_inputs = 3

# SPICE critical function generator parameters
input_names  = ['A_in','B_in','Ci_in']
critout_name = 'S_bar_out'
def critout_str(input_list):
	ins = [int(input_list[_]) for _ in range(num_inputs)]
	return ~(ins[0] ^ ins[1] ^ ins[2])

# SPICE simulation parameters (all times in ps)
Vdd   = 1       # rail voltage
T0    = 1000    # time of PWL initiation
T     = 5000    # time per combination (i.e. pulse width)
dt    = 200     # rise & fall time
dvtol = 0.5     # fractional voltage tolerance for static hazards due to contamination

# environment variables
pm_file_path = "/home/vasid/.git/courses/dic_proj/22nm_HP.pm"



# ---GENERATOR CODE---
# Part 1: Input space exploration
def generate_input_sequence(num_inputs):
	input_combs     = []
	input_changes   = []
	
	visitedtable    = []
	explored        = 1
	not_explored    = 0
	
	for i in range(2**num_inputs):
		visitedtable.append([explored])
		for j in range(1,2**num_inputs):
			visitedtable[i].append(not_explored)
	
	# initial inputs
	state  = 0
	change = 0
	i=0
	
	while i<2**num_inputs:
		input_combs.append(binary_repr(state,num_inputs))
		input_changes.append(binary_repr(change,num_inputs))
		i = 0
		while i<2**num_inputs:
			iter_state = (state+i)%(2**num_inputs)
			try:
				# look for an unexplored change in current state (i.e. input combination)
				change = visitedtable[iter_state].index(not_explored)
				visitedtable[iter_state][change] = explored
				# change to state
				state = iter_state ^ change
				# stop the loop
				break
			except:
				# look for a state with an unexplored change
				i += 1
	
	return input_combs,input_changes

input_combs,input_changes = generate_input_sequence(num_inputs)
Ncombs = len(input_combs)

# Part 2: SPICE PWL wrapper
header = "*** HEADER\n.include %s\n.params Vdd=%f\nvdd vdd gnd dc {Vdd}\n\n"%(pm_file_path,Vdd)


pwlcode = "*** PWLCODE\n"
for i in range(num_inputs):
	t = T0
	pwlcode += "Vin%d %s gnd PWL(%dp 0 "%(i,input_names[i],t)
	for j in range(Ncombs):
		pwlcode += "%dp {%d*Vdd} %dp {%d*Vdd} "%(t+dt,int(input_combs[j][i]),t+T,int(input_combs[j][i]))
		t += T
	pwlcode += ")\n\n"


meascode = "*** MEASCODE\n"
t = T0 + T
critval_old = critout_str(input_combs[0])
for i in range(1,Ncombs):
	critval = critout_str(input_combs[i])
	
	if critval==critval_old:
		critoutVsense = dvtol if critval==0 else (1-dvtol)
		critoutCross  = 2
	else:
		critoutVsense = 0.5
		critoutCross  = 1
	
	meascode += ".meas tran delay_%d trig V(%s)={%f*Vdd} td=%dp cross=%d targ V(%s)={%f*Vdd} td=%dp cross=%d\n"\
	%(i,input_names[input_changes[i].index('1')],0.5,t,1,critout_name,critoutVsense,t,critoutCross)
	
	critval_old = critval
	t+=T
meascode += "\n"


Tsim = 2*T0 + Ncombs*T
footer = "*** FOOTER\n.tran 0 %dp UIC\n"%(Tsim)


outcode = header+'\n'+pwlcode+'\n'+meascode+'\n'+footer
try:
	f = open(argv[1],"w")
	f.write(outcode)
	f.close()
except:
	print(outcode)
