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
cat $1|grep -A `echo "$nions+1"|bc` "POSITION">pos-force.tmp
awk '/--/{flag=1;next}/--/{flag=0}flag' pos-force.tmp>pos-force_new.tmp
mv pos-force_new.tmp pos-force.tmp
echo "POSITION                                       TOTAL-FORCE (eV/Angst)">pos-force_new.tmp
cat pos-force.tmp>>pos-force_new.tmp
mv pos-force_new.tmp pos-force.tmp
echo " POSITION                                       TOTAL-FORCE (eV/Angst)">>pos-force.tmp
cat $1|grep -A 3 "direct lattice vectors">lattice.tmp
echo "--">lattice_new.tmp
cat lattice.tmp>>lattice_new.tmp
mv lattice_new.tmp lattice.tmp
awk '/--/{flag=1;next}/--/{flag=0}flag' lattice.tmp>lattice_new.tmp
mv lattice_new.tmp lattice.tmp
cat lattice.tmp|sed -n "5,`echo "$nconfig*4+4"|bc`"p>lattice_new.tmp
mv lattice_new.tmp lattice.tmp
echo "      direct lattice vectors                 reciprocal lattice vectors">>lattice.tmp
cat $1|grep "free  energy   TOTEN  =">energy.tmp
cat $1|grep VRHFIN|awk -F ":" '{print $1}'|awk -F "=" '{print $2}'>atom_type.tmp
atom_num=`cat atom_type.tmp|wc -l`
for ((j=1; j<=${atom_num}; j++ )){
atom_n=`cat $1|grep "ions per type"|awk -F "=" '{print $2}'|awk -v var="$j" -F " " '{print $var}'`
echo $atom_n
}
fi
