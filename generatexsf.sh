#!/bin/bash
outcars=`find . -name OUTCAR|wc -l`
root_dir=`pwd`
for (( i=1; i<=$outcars; i++ )){
outcarfile=`find . -name OUTCAR|sed -n ${i}p|awk -F "O" '{print $1}'`
cp ./mdoutcar2xsf.sh $outcarfile
echo $outcarfile
cd $outcarfile
chmod +x ./mdoutcar2xsf.sh
./mdoutcar2xsf.sh OUTCAR
wait $!
cd ${root_dir}
}
