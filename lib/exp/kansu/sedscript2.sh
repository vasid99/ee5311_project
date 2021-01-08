#!/bin/bash
ln=0
b=0
cp project_kansu3.jelib psed0
while [ $ln -lt 64 ];do
	ln1=$(($ln/8))
	ln2=$(($ln%8))
	
	sed "s/Awire|net@[0-9]*\([0-9|]*\)pin@\([0-9|\.\-]*\)nand1x@$ln|Y|\(.*\)/Awire|~x$ln1\y$ln2\1pin@\2nand1x@$ln|Y|\3/" psed$b >psed$((1-$b))
	b=$((1-$b))
	
	sed "s/Awire|net@[0-9]*\([0-9|]*\)nand1x@$ln|Y|\(.*\)/Awire|~x$ln1\y$ln2\1nand1x@$ln|Y|\2/" psed$b >psed$((1-$b))
	b=$((1-$b))
	
	sed "s/Awire|net@[0-9]*\([0-9|]*\)pin@\([0-9|\.\-]*\)and1x@$ln|Y|\(.*\)/Awire|x$ln1\y$ln2\1pin@\2and1x@$ln|Y|\3/" psed$b >psed$((1-$b))
	b=$((1-$b))
	
	sed "s/Awire|net@[0-9]*\([0-9|]*\)and1x@$ln|Y|\(.*\)/Awire|x$ln1\y$ln2\1and1x@$ln|Y|\2/" psed$b >psed$((1-$b))
	b=$((1-$b))
	
	ln=$(($ln+1))
done
mv psed$b project_kansu4.jelib
rm psed*
