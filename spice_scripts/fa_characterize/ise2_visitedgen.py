# input space exploration
from collections import defaultdict
from numpy import binary_repr

num_inputs = 3

def print_table(vt):
	str = ''
	for i in vt:
		str += '%d\t'%i
		for j in vt[i]:
			str += ('1' if vt[i][j] else '0')+' '
		str += '\n'
	return str

visitedtable = defaultdict(list)
for i in range(2**num_inputs):
	for j in range(2**num_inputs):
		visitedtable[i].append(False)

state = 0
visitedctr = 0
N = 0

while visitedctr < 2**num_inputs:
	change = 1
	while change < 2**num_inputs:
		if visitedtable[state][change]==False:
			visitedtable[state][change] = True
			break
		change += 1
	
	if change==2**num_inputs:
		print("All states visited for foll. iteration:")
		change = state ^ (state + 1)%(2**num_inputs)
		state = (state + 1)%(2**num_inputs)
		visitedctr += 1
	else:
		state = state^change
		visitedctr = 0
	
	print("%d\t"%(N)+binary_repr(state,num_inputs)+'\t'+binary_repr(change,num_inputs))
	print(print_table(visitedtable))
	N += 1

