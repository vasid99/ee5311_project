#!/bin/bash
ln=0
b=0
cp project_kansu2.jelib psed0
while [ $ln -lt 64 ];do
	ln1=$(($ln/8))
	ln2=$(($ln%8))
	
	sed "s/Awire|net@[0-9]*\([0-9|]*\)pin@\([0-9|\.\-]*\)fa_c3x_s2x@$ln|Co_bar|\(.*\)/Awire|FA$ln1\_$ln2\_Co_bar\1pin@\2fa_c3x_s2x@$ln|Co_bar|\3/" psed$b >psed$((1-$b))
	b=$((1-$b))
	
	sed "s/Awire|net@[0-9]*\([0-9|]*\)nand1x@$ln|Co_bar|\(.*\)/Awire|FA$ln1\_$ln2\_Co_bar\1nand1x@$ln|Co_bar|\2/" psed$b >psed$((1-$b))
	b=$((1-$b))
	
	sed "s/Awire|net@[0-9]*\([0-9|]*\)pin@\([0-9|\.\-]*\)fa_c3x_s2x@$ln|S_bar|\(.*\)/Awire|FA$ln1\_$ln2\_S_bar\1pin@\2fa_c3x_s2x@$ln|S_bar|\3/" psed$b >psed$((1-$b))
	b=$((1-$b))
	
	sed "s/Awire|net@[0-9]*\([0-9|]*\)and1x@$ln|S_bar|\(.*\)/Awire|FA$ln1\_$ln2\_S_bar\1and1x@$ln|S_bar|\2/" psed$b >psed$((1-$b))
	b=$((1-$b))
	
	ln=$(($ln+1))
done
mv psed$b project_kansu3.jelib
rm psed*
