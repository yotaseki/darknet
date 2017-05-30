#!/bin/bash

# --- 教師データ ---
TESTDATA=$1
# --- フォルダの指定 ---
PREDICT=$2
C=0
for t in ${TESTDATA}
do
	for p in ${PREDICT}
	do
		export C=`expr ${C} + 1`
		d=`basename ${p}`
		DIR_NAME="Log/log_${d}_threshold"
		LIST="
		thre000  thre034  thre068
		thre001  thre035  thre069
		thre002  thre036  thre070
		thre003  thre037  thre071
		thre004  thre038  thre072
		thre005  thre039  thre073
		thre006  thre040  thre074
		thre007  thre041  thre075
		thre008  thre042  thre076
		thre009  thre043  thre077
		thre010  thre044  thre078
		thre011  thre045  thre079
		thre012  thre046  thre080
		thre013  thre047  thre081
		thre014  thre048  thre082
		thre015  thre049  thre083
		thre016  thre050  thre084
		thre017  thre051  thre085
		thre018  thre052  thre086
		thre019  thre053  thre087
		thre020  thre054  thre088
		thre021  thre055  thre089
		thre022  thre056  thre090
		thre023  thre057  thre091
		thre024  thre058  thre092
		thre025  thre059  thre093
		thre026  thre060  thre094
		thre027  thre061  thre095
		thre028  thre062  thre096
		thre029  thre063  thre097
		thre030  thre064  thre098
		thre031  thre065  thre099
		thre032  thre066  thre100
		thre033  thre067
		"
		for i in ${LIST} ;do
				PREDICTS="${p}/${i}"
				SUB_DIR=`basename ${PREDICTS}`
				echo " ---  "
				echo "PREDICT[${PREDICTS}] TESTDATA[${TESTDATA}]"
				mkdir -p ${DIR_NAME}
				OUTPUT="${DIR_NAME}/${i}"
				python test_highscore.py ${PREDICTS} ${TESTDATA} --output ${OUTPUT}
		done
		mv sheet.csv ${DIR_NAME}/sheet${C}.csv
	done
done
