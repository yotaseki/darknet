#!/usr/bin/env python
import sys ,os
import datetime
import argparse
import numpy as np

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
        self.result = self.calcIoU(self.sq1, self.sq2)

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

def calc_distance(a, b):
    cx1 = (a[0]+a[2])/2
    cy1 = (a[1]+a[3])/2
    cx2 = (b[0]+b[2])/2
    cy2 = (b[1]+b[3])/2
    d = np.sqrt((cx1-cx2)**2 + (cy1-cy2)**2)
    return d

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
# each class
    for cls in range(len(yolo)):
        AP = []
        mAP = .0
        NumTP = 0
        NumTN = 0
        NumLE = 0
        NumFP = 0
        NumFN = 0
        numBbox = 0
# each file
        for i in range(len(predict)):
            # print "loading :" + predict[i]
            if os.path.isfile(predict[i]) == False:
                #print "continue"
                continue
            if os.path.isfile(gt[i]) == False:
                #print "continue"
                continue
# each line
            p_lines = []
            g_lines = []
            for pline in open(predict[i]).readlines():
                pl = pline[:-1].split(' ')
                p_lines.append(pl)
            for gline in open(gt[i]).readlines():
                gl = gline[:-1].split(' ')
                g_lines.append(gl)
            for p in p_lines:
                if int(p[0]) == cls:
                    numBbox = numBbox+1
                    p_rect = [int(p[1]),int(p[2]),int(p[3]),int(p[4])]
                    distance = 10000000
                    for g in g_lines:
                        if int(g[0]) == cls:
                            g_rect = [int(g[1]),int(g[2]),int(g[3]),int(g[4])]
                            d = calc_distance(p_rect, g_rect)
                            if distance > d:
                                c = CalcIoU(p_rect, g_rect)
                                distance = d
                        elif int(g[0]) == -1:
                            NumFP = NumFP + 1
                            AP.append(0)
                            break
                    if c.result == "TP":
                        NumTP = NumTP + 1
                        AP.append(c.IoU)
                    if c.result == "FP":
                        NumFP = NumFP + 1
                        AP.append(c.IoU)
                    if c.result == "LE":
                        NumLE = NumLE + 1
                        AP.append(c.IoU)
                elif int(p[0]) == -1:
                    for g in g_lines:
                        if int(g[0]) == -1:
                            NumTN = NumTN + 1
                        elif int(g[0]) == cls:
                            NumFN = NumFN + 1
                            AP.append(0)
        mAP = average(AP)
        sheet = open("sheet_"+yolo[cls][0]+".csv","a")
        sheet.write("{},{},{},{},{},{},{},{}\n".format(arg.predict, mAP, NumTP, NumTN, NumFP, NumFN, NumLE, numBbox))
        #sheet.write("{}:{},{},{},{},{},{},{}\n".format(arg.predict,mAP, NumTP, NumFP,num_predict_bbox, NumTP, NumFN ,num_gt_bbox))
        
        if ((NumTP+ NumLE + NumFP) and (NumTP + NumLE + NumFN)):
            sheet_pr = open("sheet_"+yolo[cls][0]+"_PRcurve.csv","a")
            precision = float(NumTP+NumLE)/(NumTP+NumLE+NumFP)
            recall = float(NumTP+NumLE) /(NumTP+NumLE+NumFN)
            sheet_pr.write("{},{},{}\n".format(arg.predict, precision, recall))
        #print "[gt]mAP:{},TP:{},TN:{},LE{},FP{},FN{}".format(mAP[0],cntTP[0],cntTN[0],cntLE[0],cntFP[0],cntFN[0])
        #print "[pr]mAP:{},TP:{},TN:{},LE{},FP{},FN{}".format(mAP[1],cntTP[1],cntTN[1],cntLE[1],cntFP[1],cntFN[1])
        #sheet1.write("{},{},{},{},{},{},{}\n".format(arg.predict,mAP[0],cntTP[0],cntTN[0],cntLE[0],cntFP[0],cntFN[0]))
        #sheet2.write("{},{},{},{},{},{},{}\n".format(arg.predict,mAP[1],cntTP[1],cntTN[1],cntLE[1],cntFP[1],cntFN[1]))

if __name__=='__main__':
    arg = parse_arg()
    mAP= 0
    main()
