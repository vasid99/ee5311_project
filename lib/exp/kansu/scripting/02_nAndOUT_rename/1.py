'''
name outputs of every AND and NAND gate
'''
print("cp project_kansu2.jelib psed0")
b=False
for i in range(64):
	i1 = i%8
	i2 = i//8
	print("sed \"s/Awire|net@[0-9]*\\([0-9|]*\\)pin@\\([0-9|\\-\\.]*\\)nand1x@%d|Y|\\(.*\\)/Awire|~x%dy%d\\1pin@\\2nand1x@%d|Y|\\3/\" psed%d>psed%d"%(i,i1,i2,i,b,~b))
	b=~b
	print("sed \"s/Awire|net@[0-9]*\\([0-9|]*\\)nand1x@%d|Y|\\(.*\\)/Awire|~x%dy%d\\1nand1x@%d|Y|\\2/\" psed%d>psed%d"%(i,i1,i2,i,b,~b))
	b=~b
	print("sed \"s/Awire|net@[0-9]*\\([0-9|]*\\)pin@\\([0-9|\\-\\.]*\\)and1x@%d|Y|\\(.*\\)/Awire|x%dy%d\\1pin@\\2and1x@%d|Y|\\3/\" psed%d>psed%d"%(i,i1,i2,i,b,~b))
	b=~b
	print("sed \"s/Awire|net@[0-9]*\\([0-9|]*\\)and1x@%d|Y|\\(.*\\)/Awire|x%dy%d\\1and1x@%d|Y|\\2/\" psed%d>psed%d"%(i,i1,i2,i,b,~b))
	b=~b
print("mv psed%d project_kansu3.jelib\nrm psed*"%(b))

# Awire|net@[0-9]*\([0-9|]*\)pin@\([0-9|\-\.]*\)nand1x@%d|Y\(.*\)
# Awire|net@[0-9]*\([0-9|]*\)nand1x@%d|Y\(.*\)
# Awire|~x%dy%d\1pin@\2nand1x@%d|Y|\3
# Awire|net@885|||900|nand1x@6|Y|-81.5|137.5|pin@325||-81.5|135.5
# Awire|net@886|||2700|pin@330||-113.5|135.5|and1x@7|Y|-113.5|137
