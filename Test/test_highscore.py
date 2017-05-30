#!/usr/bin/env python
import sys ,os
import datetime
import argparse

LABELS = {
        "ball":0,
        "goalpost":1
        }

def getDateTime():
    d = datetime.datetime.today()
    date = '{}{}{}{}{}'.format(d.year, '%02d' % d.month, '%02d' % d.day, '%02d' % d.hour, '%02d' % d.minute)
    return date

def parse_arg():
    parser = argparse.ArgumentParser(description='test_highest_mAP.py <predicts> <teachers> --output <filename>')
    parser.add_argument('predicts'
            ,help='PATH to Predicts dir')
    parser.add_argument('teachers'
            ,help='PATH to Teacher dir')
    parser.add_argument('--label',default=0
            ,help='label')
    parser.add_argument('--output',default=""
            ,help='Name of text output')
    args = parser.parse_args()
    args.output = args.output + "log" + getDateTime() + ".txt"
    return args

class CalcIoU:
    def __init__(self,rect1,rect2):
        self.sq1 = self.Square(rect1)
        self.sq2 = self.Square(rect2)
        self.IoU = self.calcIoU()
    
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
                return -1
            if(rect[3] <= rect[1]):
                return -1
            return (rect[2]-rect[0])*(rect[3]-rect[1])
    
    def overlap(self, s1, s2):
        X1 = max(s1.x1, s2.x1)
        Y1 = max(s1.y1, s2.y1)
        X2 = min(s1.x2, s2.x2)
        Y2 = min(s1.y2, s2.y2)
        if (X1 > X2) and (Y1 > Y2):
            ovl = self.Square([-1,-1,-1,-1])
            return ovl
        ovl = self.Square([X1,Y1,X2,Y2])
        return ovl
    
    def calcIoU(self):
        if self.sq1.area == -1:
            if self.sq2.area == -1:
                return -2 #TrueNegative
            else:
                return -3 #FalseNegative
        if self.sq2.area == -1:
            return -1 #FalsePositive
        ovl = self.overlap(self.sq1, self.sq2)
        if (ovl.area == -1):
            return -1 #FalsePositive
        area_union = ovl.area
        area_total = self.sq1.area + self.sq2.area - area_union
        IoU = float(area_union) / area_total
        return IoU

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

def main():
    cnt_TP = 0
    cnt_TN = 0
    cnt_FP = 0
    cnt_FN = 0
    cnt_Lo = 0
    mAP = 0
    log = open(arg.output,'w')
    p = os.listdir(arg.predicts)
    p.sort()
    for pred in p:
        log_mesg = pred
        teac = pred.rstrip('_predict.txt')
        teac = teac + ".txt"
        pred = arg.predicts + "/" + pred
        teac = arg.teachers + "/" + teac
        if os.path.isfile(pred) == False:
            continue
        if os.path.isfile(teac) == False:
            continue
        rank = []
        IoU=0
        for line_p in open(pred).readlines():
            data_p = line_p[:-1].split(' ')
            pred_rect = [int(data_p[1]),int(data_p[2]),int(data_p[3]),int(data_p[4])]
            for line_t in open(teac).readlines():
                data_t = line_t[:-1].split(' ')
                teac_rect = [int(data_t[1]),int(data_t[2]),int(data_t[3]),int(data_t[4])]
                dst = CalcIoU(pred_rect, teac_rect)
                rank.append(dst.IoU)
        IoU = average(rank)
        if IoU == -1 or (0 < IoU and IoU < 0.1):
            if not (IoU == -1):
                log_mesg = str(IoU) + log_mesg
            log_mesg = "FP " + log_mesg
            cnt_FP = cnt_FP+1
        elif IoU == -2:
            log_mesg = "TN " + log_mesg
            cnt_TN = cnt_TN+1
        elif IoU == -3:
            log_mesg = "FN " + log_mesg
            cnt_FN = cnt_FN+1
        elif IoU < 0.5:
            log_mesg = "Lo " + str(IoU) + " " + log_mesg
            cnt_Lo = cnt_Lo+1
            mAP = mAP + IoU
        else:
            log_mesg = "TP " + log_mesg + " " + str(IoU)
            cnt_TP = cnt_TP+1
            mAP = mAP + IoU
        log.write(log_mesg + "\n")
    if (cnt_TP + cnt_Lo):
        mAP = float(mAP) / (cnt_TP + cnt_Lo)
    result = []
    result.append("mAP " + str(mAP))
    result.append("TruePositive " + str(cnt_TP))
    result.append("TrueNegative " + str(cnt_TN))
    result.append("LocalizeError " + str(cnt_Lo))
    result.append("FalsePositive " + str(cnt_FP))
    result.append("FalseNegative " + str(cnt_FN))
    sheet = open("sheet.csv","a")
    sheet.write(str(arg.output)+","+str(mAP)+","+str(cnt_TP)+","+str(cnt_TN)+","+str(cnt_Lo)+","+str(cnt_FP)+","+str(cnt_FN)+"\n")
    print " --- "
    for line in result:
        print line
        log.write(line + "\n")

if __name__=='__main__':
    arg = parse_arg()
    main()
