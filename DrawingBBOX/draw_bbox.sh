#export TEC="/home/yota/Desktop/RCNNTEST/bbox_teacher"
#export IMG="/home/yota/Desktop/DatasetsRCNN/20160817_ad/Images"
export PREDICT="$1"
export TEC="$2"
#export IMG="/mnt/Trancend2T/hdd/workspace/git/darknet/Dataset/archive/Training_data_goalpost/images"
export IMG="robocup2017_detection/images"
#export OUT_G="out_groundtruth"
#mkdir $OUT_G
export OUT_P="out_predict"
mkdir $OUT_P
for a in `ls $1 | sed "s/_predict.txt//"`
do
#    ./draw_bbox $1/${a}_predict.txt ${TEC}/${a}.txt ${IMG}/${a}.jpg 1 ${OUT_G}/${a}
    ./draw_bbox $1/${a}_predict.txt ${TEC}/${a}.txt ${IMG}/${a}.jpg 2 ${OUT_P}/${a}
done
