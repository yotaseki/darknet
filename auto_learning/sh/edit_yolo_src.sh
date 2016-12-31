#!/bin/sh

# editable
INPUT=$2
COL_NUMBER=$1 #25, 26

# 
TARGET_FILE=~/darknet/src/yolo.c

sed -i ${COL_NUMBER}d ${TARGET_FILE}
sed -i "${COL_NUMBER}i ${INPUT}" ${TARGET_FILE}
