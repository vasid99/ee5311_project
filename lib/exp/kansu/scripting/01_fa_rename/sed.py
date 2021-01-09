f=open("sedscript.sh","w")
b=False
f.write("cp project_kansu2.jelib psed0\n")
f.write("sed \"s,fa_c3x_s2x@%d,fa_c3x_s2x@%d_%d,g\" psed%d>psed%d\n"%(26,0,0,b,~b))
b=~b
for i in range(1,64):
	f.write("sed \"s,fa_c3x_s2x@%d,fa_c3x_s2x@%d_%d,g\" psed%d>psed%d\n"%(89+i,i//8,i%8,b,~b))
	b=~b
f.write("mv psed%d project_kansu3.jelib\nrm psed*"%(b))
f.close()
'''
	
	sed "s/Awire|net@[0-9]*\([0-9|]*\)pin@\([0-9|\.\-]*\)fa_c3x_s2x@$ln|Co_bar|\(.*\)/Awire|FA$ln1\_$ln2\_Co_bar\1pin@\2fa_c3x_s2x@$ln|Co_bar|\3/" psed$b >psed$((1-$b))
	b=$((1-$b))
	
	sed "s/Awire|net@[0-9]*\([0-9|]*\)fa_c3x_s2x@$ln|Co_bar|\(.*\)/Awire|FA$ln1\_$ln2\_Co_bar\1fa_c3x_s2x@$ln|Co_bar|\2/" psed$b >psed$((1-$b))
	b=$((1-$b))
	
	sed "s/Awire|net@[0-9]*\([0-9|]*\)pin@\([0-9|\.\-]*\)fa_c3x_s2x@$ln|S_bar|\(.*\)/Awire|FA$ln1\_$ln2\_S_bar\1pin@\2fa_c3x_s2x@$ln|S_bar|\3/" psed$b >psed$((1-$b))
	b=$((1-$b))
	
	sed "s/Awire|net@[0-9]*\([0-9|]*\)fa_c3x_s2x@$ln|S_bar|\(.*\)/Awire|FA$ln1\_$ln2\_S_bar\1fa_c3x_s2xx@$ln|S_bar|\2/" psed$b >psed$((1-$b))
	b=$((1-$b))'''
