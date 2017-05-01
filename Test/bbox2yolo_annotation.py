#!/usr/bin/env python
import sys ,os
import argparse

img_size = [640,480]

def parse_arg():
    parser = argparse.ArgumentParser(description='Test_bbox2yolo')
    parser.add_argument('text'
            ,help='Text having Integer position.')
    parser.add_argument('--option',default=0
            ,help='0:bbox2yolo ,1:yolo2bbox')
    parser.add_argument('--output',default='a.txt'
            ,help='Output text having float position. [default=a.txt]')
    args = parser.parse_args()
    return args

def bbox2yolo(rect):
    yolo = [0,0,0,0,0]
    yolo[0] = int(rect[0])
    yolo[1] = ((rect[3] + rect[1])/2)/img_size[0]
    yolo[2] = ((rect[4] + rect[2])/2)/img_size[1]
    yolo[3] = (rect[3] - rect[1])/img_size[0]
    yolo[4] = (rect[4] - rect[2])/img_size[1]
    return yolo

def yolo2bbox(rect):
    bbox = [0,0,0,0,0]
    bbox[0] = int(rect[0])
    x = rect[1] * img_size[0]
    y = rect[2] * img_size[1]
    w = rect[3] * img_size[0]
    h = rect[4] * img_size[1]
    bbox[1] = int(x - w/2)
    bbox[2] = int(y - h/2)
    bbox[3] = int(x + w/2)
    bbox[4] = int(y + h/2)
    return bbox


def main():
    #print(arg.bbox)
    #print(arg.output)
    src = open(arg.text,'r').readlines()
    dst = open(arg.output,'w')
    for l in src:
        data = l.split(' ')
        rect  = [0,0,0,0,0]
        for i in range(5):
            rect[i] = float(data[i])
            #print rect[i]
        #print rect
        if int(arg.option) == 0:
            print "[Run {}] int -> float [OUT {}]".format(arg.text,arg.output),
            out = bbox2yolo(rect)
        if int(arg.option) == 1:
            print "[Run {}] float -> int [OUT {}]".format(arg.text,arg.output),
            out = yolo2bbox(rect)
        #print out
        for i in range(5):
            dst.write(str(out[i]) + " ")
        dst.write("\n")
    print "... complete."

if __name__=='__main__':
    arg = parse_arg()
    main()

