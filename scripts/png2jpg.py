#!/usr/bin/env python 
import sys, os
import cv2

argv = sys.argv

print "convert :" + argv[1]
fn = argv[1]
img = cv2.imread(fn)
fn = fn.rstrip(".png") + ".jpg"
print "generate :" + fn
cv2.imwrite(fn ,img)
