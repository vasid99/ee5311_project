# input space exploration
valdict  = {'0':'0','1':'1','U':'1','D':'0'}
nextdict = {'0':'U','1':'D','U':'D','D':'U'}

def nextcomb(comb,i):
	ncomb = comb.copy()
	ncomb[i]=nextdict[comb[i]]
	return ncomb

curr = ['0','0','0']
visited=[]
visited.append(curr)
for N in range(100):
	for i in range(3):
		ncomb_i = nextcomb(curr,i)
		if ncomb_i not in visited:
			visited.append(ncomb_i)
			curr = ncomb_i
			print(curr)
			break
		
