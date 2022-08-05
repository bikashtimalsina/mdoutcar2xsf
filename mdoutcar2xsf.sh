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
if [ -d "./xsf" ]
then
rm -rf ./xsf
fi
mkdir ./xsf
for (( i=1; i<=$nconfig; i++ )){
echo "# total energy= `cat energy.tmp|sed -n ${i}p|awk -F "=" '{print $2}'`" >> ./xsf/structure${i}.xsf
echo "                                      " >> ./xsf/structure${i}.xsf
echo "CRYSTAL" >> ./xsf/structure${i}.xsf
echo "PRIMVEC" >> ./xsf/structure${i}.xsf 
slat=`echo "3*${i}-2"|bc`
elat=`echo "3*${i}"|bc`
cat lattice.tmp|sed -n "${slat},${elat}"p >> ./xsf/structure${i}.xsf
echo "PRIMCOORD" >> ./xsf/structure${i}.xsf
echo "${nions} 1" >> ./xsf/structure${i}.xsf
pfstart=`echo "(${i}-1)*${nions}+1"|bc`
pfend=`echo "${nions}*${i}"|bc`
#echo "$pfstart $pfend"
sed -n "${pfstart},${pfend}"p pos-force.tmp > posfor.tmp
paste -d' ' atom_print.tmp posfor.tmp > pos_new.tmp
cat pos_new.tmp >> ./xsf/structure${i}.xsf
}
rm *.tmp
fi
