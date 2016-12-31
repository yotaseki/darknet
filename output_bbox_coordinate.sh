#! /bin/sh
# $1 :cfg
# $2 :weight
# $3 :images dir
echo " --- list --- "
ls -d backup/random*/* |grep final |grep 00
echo " ------------ "
echo -n "OK?(y/n)"
read c

if [ $c = 'y'] ;then
	for i in `ls -d backup/random*/* |grep final |grep 00`
	do
		OUTPUT=`dirname $2 |sed "s;backup/;;"`
		OUTPUT=${OUTPUT}_predicts
		mkdir ${OUTPUT}
		./darknet_output yolo test $1 $2 $3
		mv $3/*predict.txt ${OUTPUT}/
		rename 's/.jpg//' ${OUTPUT}/*txt
		rename 's/.png//' ${OUTPUT}/*txt
	done
fi
