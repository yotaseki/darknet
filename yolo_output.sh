
# $1 :cfg
# $2 :images dir 
echo " --- list --- "
ls -d backup/random*/* |grep final |grep 0_
#ls -d backup/iriesan/*
echo " ------------ "
echo "RUN:"
for i in `ls -d backup/random*/* |grep final |grep 0_`
#for i in `ls -d backup/iriesan/*`
do
	echo "./darknet_output yolo test $1 $i $2"
done

echo -n "OK?(y/n)"
read c

if [ $c == 'y' ] ;then
	for i in `ls -d backup/random*/* |grep final |grep 0_`
	#for i in `ls -d backup/iriesan/*`
	do
		echo $i
		echo "----------------------"
		OUTPUT=`dirname $i |sed "s;backup/;;"`
		CFG=`basename $1 |sed "s/.cfg//"`
		OUTPUT=$CFG_${OUTPUT}_predicts
		mkdir ${OUTPUT}
		./darknet_output yolo test $1 $i $2
		mv $2/*predict.txt ${OUTPUT}/
		rename 's/.jpg//' ${OUTPUT}/*txt
		rename 's/.png//' ${OUTPUT}/*txt
	done
fi
