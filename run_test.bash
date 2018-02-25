#!/bin/bash
WEIGHT=$1
TEST=$2
BACKUP=$3
./darknet yolo bbox cfg/tiny-yolo_cit.cfg $WEIGHT $TEST $BACKUP
