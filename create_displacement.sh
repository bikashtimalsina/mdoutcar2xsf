#!/bin/bash
snapdirCnt=`find ./EachDisplacement -name "snaps.inp"|wc -l`
for (( i=1; i<=$snapdirCnt; i++)){
snapdironly=`find ./EachDisplacement -name "snaps.inp"|sed -n ${i}p|awk -F "/" '{print $3}'`
snapdir=`echo "./EachDisplacement/${snapdironly}"`
cd $snapdir
snaps.x
wait $!
gnuplot ~/snapshotsc4/histogram.gp
#snapc=`ls snap_0[0-9][1-9]*.xyz|wc -l`
#for (( j=1; j<=$snapc; j++ )){
#snapf=`ls snap_0[0-9][1-9]*.xyz|sed -n ${j}p`
#snapfTag=`echo $snapf|awk -F "." '{print $1}'|awk -F "_" '{print $2}'`
#mkdir -p ./$snapfTag
#}
cd ../..
}
