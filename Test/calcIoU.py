#!/usr/bin/env python
import sys ,os
import datetime
import argparse

LABELS ={
        "ball":0,
        "goalpost":1
        }

def getDateTime():
    d = datetime.datetime.today()
    date = '{}{}{}{}{}'.format(d.year, '%02d' % d.month, '%02d' % d.day, '%02d' % d.hour, '%02d' % d.minute)
    return date

def parse_arg():
    parser = argparse.ArgumentParser(description='calcIoU.py <predict> <groundtruth> --output <filename>')
    parser.add_argument('predict'
            ,help='PATH to predict text dir')
    parser.add_argument('groundtruth'
            ,help='PATH to groundtruth text dir')
    parser.add_argument('--label',default=0
            ,help='label')
    parser.add_argument('--output',default="./"
            ,help='directory log output ')
    args = parser.parse_args()
    args.output = args.output + "log_" + getDateTime() + ".txt"
    return args

class CalcIoU: # 1bbox
    def __init__(self,predict_rect,gt_rect):
        self.sq1 = self.Square(predict_rect)
        self.sq2 = self.Square(gt_rect)
        self.IoU = 0
        self.Type = self.calcIoU(self.sq1, self.sq2)

    class Square:
        def __init__(self,rect):
            self.square(rect)

        def square(self,rect):
            self.x1 = rect[0]
            self.y1 = rect[1]
            self.x2 = rect[2]
            self.y2 = rect[3]
            self.area = self.calcArea(rect)

        def calcArea(self,rect):
            if(rect[2] <= rect[0]):
                return 0
            if(rect[3] <= rect[1]):
                return 0
            return (rect[2]-rect[0])*(rect[3]-rect[1])

    def overlap(self, s1, s2):
        X1 = max(s1.x1, s2.x1)
        Y1 = max(s1.y1, s2.y1)
        X2 = min(s1.x2, s2.x2)
        Y2 = min(s1.y2, s2.y2)
        if (X1 >= X2) and (Y1 >= Y2):
            return self.Square([0,0,0,0])
        ovl = self.Square([X1,Y1,X2,Y2])
        return ovl

    def calcIoU(self, prd, gt):
        if prd.area == 0 and gt.area == 0:
            return "TN" #TrueNegative
        if prd.area == 0 and gt.area > 0 :
            return "FN" #FalseNegative
        if prd.area > 0  and gt.area == 0:
            return "FP" #FalsePositive
        ovl = self.overlap(prd,gt)
        area_overlap = ovl.area
        area_total = prd.area + gt.area - area_overlap
        IoU = float(area_overlap) / area_total
        self.IoU = IoU
        if self.IoU < 0.5:
            return "LE"
        else:
            return "TP"

class YOLO_IoU: # 1file
    def __init__(self,labelnum,MAX_THRE=0):
        self.groundtruth = []
        self.predict = []
        self.label = labelnum
        self.MAX_THRE = MAX_THRE
        self.IoU_based_on_gt = []
        self.IoU_based_on_pr = []
        self.Type_based_on_gt = ""
        self.Type_based_on_pr = ""

    def add_groundtruth(self,line):
        t = line[:-1].split(' ')
        if int(t[0]) == self.label:
            t_rect = [ 0 , [int(t[1]),int(t[2]),int(t[3]),int(t[4])] ]
            self.groundtruth.append(t_rect)
            self.groundtruth.sort()
            self.groundtruth.reverse()

    def add_predict(self,line):
        p = line[:-1].split(' ')
        if int(p[0]) == self.label:
            p_rect = [ [float(p[5])] , [int(p[1]),int(p[2]),int(p[3]),int(p[4])] ]
            self.predict.append(p_rect)
            self.predict.sort()
            self.predict.reverse()
            if self.MAX_THRE:
                while len(self.predict) > 1:
                    self.predict.pop()

    def calcIoU_based_on_gt(self):
        dummy = [[-1],[-1,-1,-1,-1]]
        if len(self.groundtruth) == 0:
            self.groundtruth.append(dummy)
        if len(self.predict) == 0:
            self.predict.append(dummy)
        for g in self.groundtruth:
            score_g = []
            for p in self.predict:
                c = CalcIoU(p[1],g[1])
                res = [c.IoU , c.Type]
                score_g.append(res)
            score_g.sort()
            score_g.reverse()
            self.IoU_based_on_gt.append(score_g[0])


    def calcIoU_based_on_predict(self):
        dummy = [[-1],[-1,-1,-1,-1]]
        if len(self.groundtruth) == 0:
            self.groundtruth.append(dummy)
        if len(self.predict) == 0:
            self.predict.append(dummy)
        for p in self.predict:
            score_p = []
            for g in self.groundtruth:
                c = CalcIoU(p[1],g[1])
                res = [c.IoU , c.Type]
                score_p.append(res)
            score_p.sort()
            score_p.reverse()
            self.IoU_based_on_pr.append(score_p[0])

def highscore(rank):
    IoU=0
    rank.sort()
    rank.reverse()
    IoU = rank[0]
    return IoU

def average(rank):
    IoU=0
    for a in rank:
        IoU += a
    IoU = float(IoU) / len(rank)
    if IoU < 0:
        IoU = int(IoU)
    return IoU

def make_predict_list(files):
    predict = []
    for fn in files:
        fn = arg.predict + "/" + fn
        predict.append(fn)
    return predict

def make_gt_list(files):
    gt = []
    for fn in files:
        fn = fn.rstrip('_predict.txt')
        fn = arg.groundtruth +"/" + fn + ".txt"
        gt.append(fn)
    return gt

def main():
    files = os.listdir(arg.predict)
    predict = make_predict_list(files)
    gt = make_gt_list(files)
    predict.sort()
    gt.sort()
    for i in range(len(predict)):
        print "loading :" + predict[i]
        if os.path.isfile(predict[i]) == False:
            print "continue"
            continue
        if os.path.isfile(gt[i]) == False:
            print "continue"
            continue
        y1 = YOLO_IoU(LABELS["ball"],1)
        y2 = YOLO_IoU(LABELS["goalpost"])
        for p_line in open(predict[i]).readlines():
            y1.add_predict(p_line)
            y2.add_predict(p_line)
        for t_line in open(gt[i]).readlines():
            y1.add_groundtruth(t_line)
            y2.add_groundtruth(t_line)
        y1.calcIoU_based_on_predict()
        y1.calcIoU_based_on_gt()
        y2.calcIoU_based_on_predict()
        y2.calcIoU_based_on_gt()
        print y2.groundtruth
        print y2.predict
        print y2.IoU_based_on_gt
        print y2.IoU_based_on_pr
        """
        log = open(arg.output)
        if dst == "FN":
            log.write(predict[i] + " FN ")
        if dst == "FP":
            log.write(predict[i] + " FP " + str(IoU))
        if dst == "TN":
            log.write(predict[i] + " TN ")
        if dst == "TP":
            log.write(predict[i] + " TP " + str(IoU))
        if dst == "LE":
            log.write(predict[i] + " LE " + str(IoU))
        """

if __name__=='__main__':
    arg = parse_arg()
    cnt_TP = 0
    cnt_TN = 0
    cnt_FP = 0
    cnt_FN = 0
    cnt_Lo = 0
    mAP= 0
    main()
