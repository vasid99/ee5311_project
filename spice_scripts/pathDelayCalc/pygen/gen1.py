print(".include \"/home/vasid/.git/courses/dic_proj/22nm_HP.pm\"\n.params Vdd=1 changetol=1m\nVdd vdd gnd dc {Vdd}\n\n",end="")
for i in range(8):
	print("Vx%d x%d gnd PULSE(0 {Vdd} 10n 200p 200p 5n 10n)\n"%(i,i),end="")

print("\n",end="")

for i in range(8):
	print("Vy%d y%d gnd PULSE(0 {Vdd} 10n 200p 200p 5n 10n)\n"%(i,i),end="")

print("\n.tran 0 40n UIC",end="")

for i in range(64):
	i1=i//8
	i2=i%8
	print(".meas tran FA_Co_bar_%d_%d_rc_delay trig  cross=1 td=8n targ V(FA_Co_bar_%d_%d)= cross=2 td=8n\n"%(i1,i2,i1,i2),end="")

for i in range(64):
	

# print("",end="")
