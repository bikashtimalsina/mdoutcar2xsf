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
echo " POSITION                                       TOTAL-FORCE (eV/Angst)">pos-force_new.tmp
cat pos-force.tmp>>pos-force_new.tmp
mv pos-force_new.tmp pos-force.tmp
echo " POSITION                                       TOTAL-FORCE (eV/Angst)">>pos-force.tmp
cat $1|grep -A 3 "direct lattice vectors">lattice.tmp
cat $1|grep -A 14 "FORCE on cell =-STRESS"|grep Total|awk -F " " '{print $2,$3,$4,$5,$6,$7}'>>virial.tmp
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
echo "The type of atom in the OUTCAR is: `cat atom_type.tmp|xargs`"
if [ -f "./atom_num.tmp" ]
then
rm atom_num.tmp
fi
atom_tag=""
atom_num_tag=""
for ((j=1; j<=${atom_num}; j++ )){
atom_n=`cat $1|grep "ions per type"|awk -F "=" '{print $2}'|awk -v var="$j" -F " " '{print $var}'`
atom_num_tag+="`echo $atom_n` "
for (( k=1; k<=${atom_n}; k++ )){
atom_tag+="`cat atom_type.tmp|sed -n ${j}p` "
}
echo $atom_n>>atom_num.tmp
}
echo "The number of each atoms in the OUTCAR is: `cat atom_num.tmp|xargs`"
awk '/direct/{flag=1;next}/direct/{flag=0}flag' lattice.tmp>lattice_new.tmp
cat lattice_new.tmp|awk '//{print $1,$2,$3}'>lattice.tmp
rm lattice_new.tmp
awk '/ POSITION/{flag=1;next}/ POSITION/{flag=0}flag' pos-force.tmp>pos-force_new.tmp
mv pos-force_new.tmp pos-force.tmp
#for vertical printing
echo $atom_tag|awk -v FS=" " -v OFS='\n' '{$1=$1}1'>atom_print.tmp
fi
if [ -d "xyz" ]
then
rm -rf xyz
fi
mkdir ./xyz
startind=1
for (( i=1; i<=$nconfig; i++ )){
dlstart=`echo "3*${i}-2"|bc`
dlend=`echo "3*${i}"|bc`
sed -n "${dlstart},${dlend}"p lattice.tmp > latvec.txt
cat latvec.txt|tr -s "\n" " " > testlattxyz.tmp
latt=`cat testlattxyz.tmp|awk -F " " '{print $1,$2,$3,$4,$5,$6,$7,$8,$9}'`
ener=`sed -n ${i}p energy.tmp|awk -F "=" '{print $2}'|awk -F " " '{print $1}'`
viri=`sed -n ${i}p virial.tmp`
echo $nions >> ./xyz/snapshots-${i}-each.xyz
echo "Lattice=\"$latt\" Energy=$ener Virial=\"$viri\" Properties=species:S:1:pos:R:3:force:R:3">>./xyz/snapshots-${i}-each.xyz
endind=`echo "$nions+$startind-1"|bc`
sed -n "$startind,$endind"p pos-force.tmp> fxyz.txt
startind=`echo "$endind+1"|bc`
paste -d " " atom_print.tmp fxyz.txt > eachf.tmp
cat eachf.tmp >> ./xyz/snapshots-${i}-each.xyz
}
rm latvec.txt
rm testlattxyz.tmp
rm *.tmp
rm *.txt
