#!/bin/bash
./run_test.bash ./Backup/weights/180218_robocup2017_3236train/tiny-yolo_cit_final.weights ./Dataset/testtxt/2class/180218_robocup2017_244test.txt Backup/test/180218_robocup2017_244test/180218_robocup2017_3236predict
./run_test.bash ./Backup/weights/180218_robocup2017_255train/tiny-yolo_cit_final.weights ./Dataset/testtxt/2class/180218_robocup2017_244test.txt Backup/test/180218_robocup2017_244test/180218_robocup2017_255predict
./run_test.bash ./Backup/weights/180218_shinnara_2981train/tiny-yolo_cit_final.weights ./Dataset/testtxt/2class/180218_robocup2017_244test.txt Backup/test/180218_robocup2017_244test/180218_shinnara_2981predict
