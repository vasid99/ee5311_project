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
