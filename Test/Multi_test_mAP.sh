#!/bin/bash

# --- 教師データ ---
TEACHER="Teacher/capet_test/"
# --- フォルダの指定 ---
PREDICT="
Predict/TEST_capet_WEIGHT_voc_bg_threshold
"
C=0
for t in ${TEACHER}
do
	for p in ${PREDICT}
	do
		export C=`expr ${C} + 1`
		d=`basename ${p}`
		DIR_NAME="log_${d}_threshold"
		LIST="
		${p}/thre000  ${p}/thre034  ${p}/thre068
		${p}/thre001  ${p}/thre035  ${p}/thre069
		${p}/thre002  ${p}/thre036  ${p}/thre070
		${p}/thre003  ${p}/thre037  ${p}/thre071
		${p}/thre004  ${p}/thre038  ${p}/thre072
		${p}/thre005  ${p}/thre039  ${p}/thre073
		${p}/thre006  ${p}/thre040  ${p}/thre074
		${p}/thre007  ${p}/thre041  ${p}/thre075
		${p}/thre008  ${p}/thre042  ${p}/thre076
		${p}/thre009  ${p}/thre043  ${p}/thre077
		${p}/thre010  ${p}/thre044  ${p}/thre078
		${p}/thre011  ${p}/thre045  ${p}/thre079
		${p}/thre012  ${p}/thre046  ${p}/thre080
		${p}/thre013  ${p}/thre047  ${p}/thre081
		${p}/thre014  ${p}/thre048  ${p}/thre082
		${p}/thre015  ${p}/thre049  ${p}/thre083
		${p}/thre016  ${p}/thre050  ${p}/thre084
		${p}/thre017  ${p}/thre051  ${p}/thre085
		${p}/thre018  ${p}/thre052  ${p}/thre086
		${p}/thre019  ${p}/thre053  ${p}/thre087
		${p}/thre020  ${p}/thre054  ${p}/thre088
		${p}/thre021  ${p}/thre055  ${p}/thre089
		${p}/thre022  ${p}/thre056  ${p}/thre090
		${p}/thre023  ${p}/thre057  ${p}/thre091
		${p}/thre024  ${p}/thre058  ${p}/thre092
		${p}/thre025  ${p}/thre059  ${p}/thre093
		${p}/thre026  ${p}/thre060  ${p}/thre094
		${p}/thre027  ${p}/thre061  ${p}/thre095
		${p}/thre028  ${p}/thre062  ${p}/thre096
		${p}/thre029  ${p}/thre063  ${p}/thre097
		${p}/thre030  ${p}/thre064  ${p}/thre098
		${p}/thre031  ${p}/thre065  ${p}/thre099
		${p}/thre032  ${p}/thre066  ${p}/thre100
		${p}/thre033  ${p}/thre067
		"
		for PREDICTS in ${LIST} ;do
				SUB_DIR=`basename ${PREDICTS}`
				echo " ---  "
				echo "PREDICT[${PREDICTS}] TEACHER[${TEACHER}]"
				#mkdir -p ${DIR_NAME}/${SUB_DIR}
				#mkdir -p "${DIR_NAME}_highscore/${SUB_DIR}"
				#python test_highscore.py ${PREDICTS} ${TEACHER} --output "${DIR_NAME}/${SUB_DIR}/${SUB_DIR}"
				python test_mAP.py ${PREDICTS} ${TEACHER} ${DIR_NAME}/${SUB_DIR}/${SUB_DIR}
				#python test_highscore.py ${PREDICTS} ${TEACHER} --output "${DIR_NAME}_highscore/${SUB_DIR}/${SUB_DIR}"
		done
		mv sheet.csv sheet${C}.csv
	done
done
