#!/bin/bash
WEIGHT=$1
TEST=$2
BACKUP=$3
./darknet yolo bboxdir cfg/tiny-yolo_2class.cfg $WEIGHT $TEST $BACKUP
