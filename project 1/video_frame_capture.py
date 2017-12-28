#-*- coding: utf-8 -*-

import cv2
import os
import cv



vc = cv2.VideoCapture('VIDEO NAME ') 
c = 1
 
if vc.isOpened():
    rval,frame = vc.read()
    print rval
else:
    rval = False
    print 0

timeF = 1000

while(rval):
    rval,frame = vc.read()
    #print frame
    # if(c%timeF == 0):
    cv2.imwrite("./PATH/" + str(c)+".jpg",frame)
    print 1
    c = c+1
    cv2.waitKey(1)
vc.release()

