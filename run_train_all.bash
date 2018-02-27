echo "[3236] `date`" >> log.txt
 ./run_train.bash Dataset/traintxt/2class/180218_robocup2017_3236train.txt Backup/weights/180218_robocup2017_3236train/
echo "[255] `date`" >> log.txt
 ./run_train.bash Dataset/traintxt/2class/180218_robocup2017_255train.txt Backup/weights/180218_robocup2017_255train/
echo "[2981] `date`" >> log.txt
 ./run_train.bash Dataset/traintxt/2class/180218_shinnara_2981train.txt Backup/weights/180218_shinnara_2981train/
echo "[7916] `date`" >> log.txt
./run_train.bash Dataset/traintxt/2class/170801_ALL_7916train.txt Backup/weights/170801_ALL_7916train
echo "[end] `date`" >> log.txt
