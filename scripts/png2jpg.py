#!/usr/bin/env python 
# DETAIL : 
# * $1 directory has image(.png)
import sys, os
import cv2

argv = sys.argv
line = os.listdir(argv[1])
for i in line:
    #print os.path.splitext(i)
    if os.path.splitext(i)[1] == '.png':
        fn = argv[1] + "/" + i
        img = cv2.imread(fn)
        fn = fn.rstrip(".png") + ".jpg"
        print "generate :" + fn
        cv2.imwrite(fn ,img)
