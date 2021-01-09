# input space exploration
from collections import defaultdict
from numpy import binary_repr
from sys import argv
import wave
import struct

num_inputs = int(argv[1])

visitedtable = defaultdict(list)
strbinout = []
strout = []

for i in range(num_inputs):
	strout.append([])

for i in range(2**num_inputs):
	for j in range(2**num_inputs):
		visitedtable[i].append(False)

state = 0
statebin = binary_repr(state,num_inputs)
print(statebin)
strbinout.append(statebin)
for i in range(num_inputs):
	strout[i].append(int(statebin[-i-1]))

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
	print(statebin)
	strbinout.append(statebin)
	for i in range(num_inputs):
		strout[i].append(int(statebin[-i-1]))

for i in range(num_inputs):
	wavout = wave.open("fa_char_inputs%d.wav"%i,"w")
	wavout.setsampwidth(1)
	wavout.setnchannels(1)
	wavout.setframerate(44100)
	for j in range(len(strout[i])):
		data = struct.pack("<b",strout[i][j]*127)
		wavout.writeframesraw(data)
	wavout.close()
