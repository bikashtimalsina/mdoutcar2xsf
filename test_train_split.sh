#!/bin/bash
if [ -f "./shuffle.txt" ];
then
rm shuffle.txt
fi
ls ./MTP-CFG|shuf > shuffle.txt
dirs=`cat shuffle.txt|wc -l`
train_count=`echo "0.9*${dirs}/1"|bc`
test_count=`echo "${dirs}-${train_count}"|bc`
for (( i=1; i<${train_count}; i++ )){
dirEach=`cat shuffle.txt|sed -n ${i}p`
cat ./MTP-CFG/$dirEach >> train.cfg
}
for (( i=${train_count}; i<=${dirs}; i++ )){
dirTest=`cat shuffle.txt|sed -n ${i}p`
cat ./MTP-CFG/$dirTest >> test.cfg
}
