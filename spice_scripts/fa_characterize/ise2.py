# input space exploration
from collections import defaultdict
from numpy import binary_repr
from sys import argv

num_inputs = int(argv[1])

visitedtable = defaultdict(list)
for i in range(2**num_inputs):
	for j in range(2**num_inputs):
		visitedtable[i].append(False)

state = 0
print(binary_repr(state,num_inputs))

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
	print(binary_repr(state,num_inputs))
