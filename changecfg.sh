#!/bin/bash
xyzc=`ls ./data/*.xyz|wc -l`
for (( i=1; i<=$xyzc; i++ )){
xyz=`ls ./data/*.xyz|sed -n ${i}p`
echo $xyz
python ~/Github/personal/mdoutcar2xsf/xyz2cfg.py $xyz
wait $!
mv out.cfg ./data/out-${i}.cfg  
}
if [ -f "./shuffle.txt" ];
then
rm ./shuffle.txt
fi
ls ./data/*.cfg|shuf > ./shuffle.txt
cfgsC=`cat ./shuffle.txt|wc -l`
echo $cfgsC
trainC=`echo "0.9*${cfgsC}/1"|bc`
echo $trainC
testC=`echo "${cfgsC}-${trainC}"|bc`
echo $testC
for (( i=1; i<$trainC; i++ )){
trainDir=`cat ./shuffle.txt|sed -n ${i}p`
cat $trainDir >> ./train.cfg
}
for (( i=$trainC; i<=$cfgsC; i++ )){
testDir=`cat ./shuffle.txt|sed -n ${i}p`
cat $testDir >> ./test.cfg
}
