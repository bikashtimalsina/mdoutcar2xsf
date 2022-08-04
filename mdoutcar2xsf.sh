#!/bin/bash
if [ -z "$1" ]
then
echo "Please provide OUTCAR file!"
fi
if [ ! -z "$1" ]
then
nconfig=`cat $1|grep POSITION|wc -l`
if [ $nconfig == 0 ]
then
echo "Please provide appropriate VASP or VASP-AIMD OUTCAR file"
exit
fi
nions=`cat $1|grep NIONS|awk -F "number of ions" '{print $2}'|awk -F "=" '{print $2}'`
echo $1
echo "The number of snapshots in the OUTCAR is: $nconfig"
echo "The number of ions in the system is: $nions"
for (( i=1; i<=$nconfig; i++ )){
cat $1|grep -A `echo "$nions+1"|bc` "POSITION">pos.tmp
}
fi
