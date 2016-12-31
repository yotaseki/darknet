DARKNET_HOME=/home/citdl/darknet
CONFIG=/home/citdl/darknet/cfg/tiny-yolo.cfg
WEIGHT=

for i in `ls -d index/* |grep index/phase |grep -v "log"`
do
	echo "*********${i}************"
	cat $i
done

echo "よろしいですか？(yes/no)"
read KEY
if [ "$KEY" == "yes" ] ;then
	for i in `ls -d index/* |grep index/phase |grep -v "log"`
	do
		cd ${DARKNET_HOME}/auto_learning
		echo " -- New phase -- "
		IMAGES=`cat $i |sed -n 1p |sed "s/IMAGES://" |sed "s/ //g"`
		BACKUP=`cat $i |sed -n 2p |sed "s/BACKUP://" |sed "s/ //g"`
		./sh/edit_yolo_src.sh 20 "    char *train_images = \"${IMAGES}\";"
		./sh/edit_yolo_src.sh 21 "    char *backup_directory = \"${BACKUP}\";"
		mv ${i} ${i}.log
		cd ${DARKNET_HOME}
		#cat ${DARKNET_HOME}/src/yolo.c |sed -n 25p
		#cat ${DARKNET_HOME}/src/yolo.c |sed -n 26p
		make -j4
		./darknet yolo train ${CONFIG} ${WEIGHT}
	done
fi
