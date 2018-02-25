#!/bin/bash
TRAINTXT=$1
BACKUP=$2
./darknet yolo train cfg/tiny-yolo_cit.cfg darknet.conv.weights $TRAINTXT $BACKUP
