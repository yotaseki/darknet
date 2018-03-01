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
        if self.IoU < 0.1:
            return "FP"
        elif self.IoU < 0.5:
            return "LE"
        else:
            return "TP"

class YOLO_IoU: # 1file
    def __init__(self,labelnum,MAX_THRE=0):
        self.groundtruth = []
        self.predict = []
        self.label = labelnum
        self.MAX_THRE = MAX_THRE
        self.based_on_gt = []
        self.based_on_pr = []
        self.AP = .0

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
            if self.MAX_THRE > 0:
                while len(self.predict) > self.MAX_THRE:
                    self.predict.pop()

    def calcIoU_based_on_gt(self):
        gt = list(self.groundtruth)
        pr = list(self.predict)
        if len(pr) == 0:
            pr.append([0,[-1,-1,-1,-1]])
        if len(gt) == 0:
            gt.append([0,[-1,-1,-1,-1]])
        for g in gt:
            score_g = []
            for p in pr:
                c = CalcIoU(p[1],g[1])
                score_g.append([c.IoU, c.Type])
            score_g.sort()
            score_g.reverse()
            self.based_on_gt.append(score_g[0])

    def calcIoU_based_on_predict(self):
        gt = list(self.groundtruth)
        pr = list(self.predict)
        if len(pr) == 0:
            pr.append([0,[-1,-1,-1,-1]])
        if len(gt) == 0:
            gt.append([0,[-1,-1,-1,-1]])
        for p in pr:
            score_p = []
            for g in gt:
                c = CalcIoU(p[1],g[1])
                score_p.append([c.IoU, c.Type])
            score_p.sort()
            score_p.reverse()
            self.based_on_pr.append(score_p[0])
        self.AP = self.AveragePrecision(self.based_on_pr)

    def AveragePrecision(self, result):
        AP = 0
        for i in result:
            AP = AP + i[0]
        if len(result) > 0:
            AP = float(AP) / len(result)
        if AP < 0:
            AP = int(AP)
        return AP

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
    if len(rank) > 0:
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
    yolo = [    # ["objectname",topN (default=0;ALL)]
        ["ball",1],
        ["goalpost",0]
    ]
    for cls in range(len(yolo)):
        AP = []
        mAP = .0
        cnt_TPpr = 0
        cnt_FPpr = 0
        cnt_LEpr = 0
        num_predict_bbox = 0
        cnt_TPgt = 0
        cnt_FNgt = 0
        cnt_LEgt = 0
        num_gt_bbox = 0
        for i in range(len(predict)):
            # print "loading :" + predict[i]
            if os.path.isfile(predict[i]) == False:
                #print "continue"
                continue
            if os.path.isfile(gt[i]) == False:
                #print "continue"
                continue
            y = YOLO_IoU(LABELS[yolo[cls][0]],yolo[cls][1])
            for p_line in open(predict[i]).readlines():
                y.add_predict(p_line)
            for g_line in open(gt[i]).readlines():
                y.add_groundtruth(g_line)
            y.calcIoU_based_on_predict()
            y.calcIoU_based_on_gt()
            ### Based on PREDICT
            result_pr = y.based_on_pr
            num_predict_bbox = num_predict_bbox + len(y.predict)
            for r in result_pr:
                if r[1] == "TP":
                    cnt_TPpr = cnt_TPpr + 1
                if r[1] == "FP":
                    cnt_FPpr = cnt_FPpr + 1
                if r[1] == "LE":
                    cnt_LEpr = cnt_LEpr + 1
            #### Based on GROUNDTRUTH
            result_gt = y.based_on_gt
            num_gt_bbox = num_gt_bbox + len(y.groundtruth)
            for r in result_gt:
                if r[1] == "TP":
                    cnt_TPgt = cnt_TPgt + 1
                if r[1] == "FN":
                    cnt_FNgt = cnt_FNgt + 1
                if r[1] == "LE":
                    cnt_LEgt = cnt_LEgt + 1
            AP.append(y.AP)
        mAP = average(AP)
        sheet = open("sheet_"+yolo[cls][0]+".csv","a")
        print "mAP:{}, TPpr:{}, FPpr:{}, NUM_pr:{}, TPgt:{}, FNgt:{}, NUM_gt:{}".format(mAP, cnt_TPpr, cnt_FPpr, num_predict_bbox, cnt_TPgt, cnt_FNgt ,num_gt_bbox)
        sheet.write("{},{},{},{},{},{},{},{},{},{}\n".format(arg.predict,mAP, cnt_TPpr, cnt_FPpr, cnt_LEpr,num_predict_bbox, cnt_TPgt, cnt_FNgt,cnt_LEgt ,num_gt_bbox))
        #sheet.write("{}:{},{},{},{},{},{},{}\n".format(arg.predict,mAP, cnt_TPpr, cnt_FPpr,num_predict_bbox, cnt_TPgt, cnt_FNgt ,num_gt_bbox))
        
        if ((cnt_TPpr+cnt_LEpr + cnt_FPpr) and (cnt_TPgt+cnt_LEgt+cnt_FNgt)):
            sheet_pr = open("sheet_"+yolo[cls][0]+"_PRcurve.csv","a")
            precision = float(cnt_TPpr+cnt_LEpr)/(cnt_TPpr+cnt_LEpr+cnt_FPpr)
            recall = float(cnt_TPgt+cnt_LEgt) /(cnt_TPgt+cnt_LEgt+cnt_FNgt)
            sheet_pr.write("{},{},{}\n".format(arg.predict, precision, recall))
        #print "[gt]mAP:{},TP:{},TN:{},LE{},FP{},FN{}".format(mAP[0],cntTP[0],cntTN[0],cntLE[0],cntFP[0],cntFN[0])
        #print "[pr]mAP:{},TP:{},TN:{},LE{},FP{},FN{}".format(mAP[1],cntTP[1],cntTN[1],cntLE[1],cntFP[1],cntFN[1])
        #sheet1.write("{},{},{},{},{},{},{}\n".format(arg.predict,mAP[0],cntTP[0],cntTN[0],cntLE[0],cntFP[0],cntFN[0]))
        #sheet2.write("{},{},{},{},{},{},{}\n".format(arg.predict,mAP[1],cntTP[1],cntTN[1],cntLE[1],cntFP[1],cntFN[1]))

if __name__=='__main__':
    arg = parse_arg()
    mAP= 0
    main()
