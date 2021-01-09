#!/bin/bash
ln=0
b=0
cp project_kansu4.jelib psed0
while [ $ln -lt 64 ];do
	ln1=$(($ln%8))
	ln2=$(($ln/8))
	
	sed "s/Awire|net@[0-9]*\([0-9|]*\)pin@\([0-9|\.\-]*\)fa_c3x_s2x@$ln|Co_bar|\(.*\)/Awire|FA$ln1\_$ln2\_Co_bar\1pin@\2fa_c3x_s2x@$ln|Co_bar|\3/" psed$b >psed$((1-$b))
	b=$((1-$b))
	
	sed "s/Awire|net@[0-9]*\([0-9|]*\)fa_c3x_s2x@$ln|Co_bar|\(.*\)/Awire|FA$ln1\_$ln2\_Co_bar\1fa_c3x_s2x@$ln|Co_bar|\2/" psed$b >psed$((1-$b))
	#      Awire|net@1021  |||0|      fa_c3x_s2x@1  |Co_bar|62|94.5|pin@521||60|94.5
	b=$((1-$b))
	
	sed "s/Awire|net@[0-9]*\([0-9|]*\)pin@\([0-9|\.\-]*\)fa_c3x_s2x@$ln|S_bar|\(.*\)/Awire|FA$ln1\_$ln2\_S_bar\1pin@\2fa_c3x_s2x@$ln|S_bar|\3/" psed$b >psed$((1-$b))
	b=$((1-$b))
	
	sed "s/Awire|net@[0-9]*\([0-9|]*\)fa_c3x_s2x@$ln|S_bar|\(.*\)/Awire|FA$ln1\_$ln2\_S_bar\1fa_c3x_s2x@$ln|S_bar|\2/" psed$b >psed$((1-$b))
	b=$((1-$b))
	
	ln=$(($ln+1))
done
mv psed$b project_kansu5.jelib
rm psed*
