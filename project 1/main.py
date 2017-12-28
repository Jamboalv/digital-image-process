# -*- coding: utf8 -*-

import argparse  
import datetime  
import imutils  
import time  
import cv2 
import numpy as np 
import os
import ast
import random
import math
import sys
from trackers import *
from detect import *


colors = [(255,0,0),(0,255,0),(0,0,255),(255,182,193),(220,20,60),(218,112,214),(128,78,128),(178,0,34),(79,0,139),
              (0,0,205),(0,0,139),(176,196,222),(30,144,255),(135,206,235),(0,139,139),(0,250,154),(143,188,143),
              (34,139,34),(255,255,224),(255,250,205),(218,165,32),(0,0,0),(178,34,34)]
 
ap = argparse.ArgumentParser()  
ap.add_argument("-v", "--video", help="path to the video file")  
ap.add_argument("-a", "--min-area", type=int, default=2000, help="minimum area size") 
ap.add_argument("-t", "--txt", help="path to the lane txt file")  
args = vars(ap.parse_args())  

class Point:
    def __init__(self,x0,y0,x1,y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1


drawing = True 
ix,iy,cx,cy = -1,-1,-1,-1
 
def draw_line(event,x,y,flags,param):
    global ix,iy,cx,cy,drawing
 
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
 
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cx,cy = x,y
    
if __name__ == '__main__':

    if args.get("video", None) is None:  
        camera = cv2.VideoCapture(0)  
        time.sleep(0.25)       
    else:  
        camera = cv2.VideoCapture(args["video"])

    if args.get("txt", None) is None:  
        print "请输入车辆轨迹txt文件路径!"     
    else:  
        txt_path = args["txt"]
    txt = open(txt_path, "r")
         
    firstFrame = None  
  
    while True:  
         
        (grabbed, frame) = camera.read()  
        text = "Unoccupied"  
        
        if not grabbed:  
            break  
          
        frame = imutils.resize(frame, width=1048)  
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
        gray = cv2.GaussianBlur(gray, (21, 21), 0)  
         
        if firstFrame is None:  
            firstFrame = gray  
            continue  

        frameDelta = cv2.absdiff(firstFrame, gray)  
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1] 

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5)) 

        opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)  

        (cnts, _) = cv2.findContours(opened.copy(), cv2.RETR_EXTERNAL,  
                                        cv2.CHAIN_APPROX_SIMPLE) 
 
        framelist = []
  
        for c in cnts:  
            # if the contour is too small, ignore it  
            if cv2.contourArea(c) < args["min_area"]:  
                continue  
          
            (x, y, w, h) = cv2.boundingRect(c)  
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2) 
            framelist.append([x, x+w, y, y+h]) 
            itemMap = updateItemMap(Item(x, x+w, y, y+h), itemMap)
            text = "Occupied"  
        
        itemMap = refreshStateflag(itemMap)    
        itemMap = clearTracing(itemMap)
        updateItemList(framelist)
      
        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),  
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),  
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)  

        for i in range(len(itemList)):
            item = itemList[i]
            if item == None:
                break
            cv2.rectangle(frame,(item.xmin,item.ymin),(item.xmax,item.ymax),colors[i%21],2)
            size = 1800
            centlength = 10
            if len(item.centers) > centlength and item.num == 0:
                num[0] += 1
                item.num = num[0]
            for j in range(1, len(item.centers))[::-1]:
                cv2.line(frame, item.centers[j-1],item.centers[j], colors[i%21],5)
                if size < 1:
                    break
                size -= 1

        cv2.namedWindow('Security Feed')  

        cv2.setMouseCallback('Security Feed',draw_line)
        cv2.line(frame,(ix,iy), (cx,cy), (0,255,255), 1)
        cv2.imshow("Security Feed",frame)
                
        cv2.imshow("Thresh", opened)  
        cv2.imshow("Frame Delta", frameDelta)  
        key = cv2.waitKey(1) & 0xFF  
          
        if key == ord("q"):  
            break

        flag = 0
        while (flag == 0):
            if (ix != -1) & (cx != -1):
                detect_press_line(txt,ix,iy,cx,cy)
                flag = flag + 1
            else:
                break  

    camera.release()  
    cv2.destroyAllWindows()  



#############################################
# 扩展阀值图像填充孔洞，然后找到阀值图像上的轮廓  
#thresh = cv2.dilate(thresh, None, iterations=2) 
# dilate = cv2.dilate(thresh, kernel)
# erode = cv2.erode(thresh, kernel)
# 将两幅图像相减获得边，第一个参数是膨胀后的图像，第二个参数是腐蚀后的图像  
# result = cv2.absdiff(dilate,erode)
# 上面得到的结果是灰度图，将其二值化以便更清楚的观察结果  
# retval, result = cv2.threshold(result, 25, 255, cv2.THRESH_BINARY);   
# 反色，即对二值图每个像素取反  
# #result = cv2.bitwise_not(result)
#######################################################################