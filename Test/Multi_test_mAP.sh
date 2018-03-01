#!/bin/bash

# --- 教師データ ---
TESTDATA=$1
# --- フォルダの指定 ---
PREDICT=$2

MAX_THRESHOLD=1000
C=0
for t in ${TESTDATA}
do
	for p in ${PREDICT}
	do
		export C=`expr ${C} + 1`
		d=`basename ${p}`
		DIR_NAME="Log/log_${d}_threshold"
        LIST=`for a in $(seq 0 $MAX_THRESHOLD);do echo $a |awk '{printf"thre%04d\n",$0}';done`
		for i in ${LIST} ;do
				PREDICTS="${p}/${i}"
				SUB_DIR=`basename ${PREDICTS}`
				echo "PREDICT[${PREDICTS}] TESTDATA[${TESTDATA}]"
				mkdir -p ${DIR_NAME}
				OUTPUT="${DIR_NAME}/${i}"
				python calcIoU3.py ${PREDICTS} ${TESTDATA} --output ${OUTPUT}
		done
		mv sheet*.csv ${DIR_NAME}/
        # sort threshold
        for s in `ls ${DIR_NAME}/*.csv`
        do
            sort ${s} -o ${s}
            sed -i "s/.*thre//" ${s}
        done
        # copy for drawing PRcurve
        for cu in `ls ${DIR_NAME} |grep curve`
        do
            cp ${DIR_NAME}/${cu} ${cu} 
            sed -i "s/.*thre...,//" ${cu}
            rename "s/sheet/${d}/" ${cu}
        done
	done
done
