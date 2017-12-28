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

itemList = []
num = [-1]

class Item:
    def __init__(self, xmin, xmax, ymin, ymax):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.stateFlag = 0
        self.findFlag = 0
        self.centers = []
        self.num = 0
        self.isNew = False     
        
def checkDis(start,end, x,y):
    a = math.sqrt((x-start[0])*(x-start[0])+(y-start[1])*(y-start[1]))
    b = math.sqrt((x-end[0])*(x-end[0])+(y-end[1])*(y-end[1]))
    c = math.sqrt((start[0]-end[0])*(start[0]-end[0])+(start[1]-end[1])*(start[1]-end[1]))
    p = (a+b+c)*0.5
    s = math.sqrt(p * (p - a) * (p - b) * (p - c))
    dis = s*2/c
    return dis    

def computerOverlap(item, item1): # return the lap area of these two item
    if(item.xmin > item1.xmin):
        itemTemp = item
        item = item1
        item1 = itemTemp
    w = item.xmax - item1.xmin     
    w = 0 if(w < 0) else w  
    if(item.ymin > item1.ymin):
        itemTemp = item
        item = item1
        item1 = itemTemp
    h = item.ymax - item1.ymin     
    h = 0 if(h < 0) else h     
    return w*h
    
def computeArea(item):    # compute the area of this rectangle
   w = item.xmax - item.xmin
   h = item.ymax - item.ymin
   return w*h   
    
global itemMap
itemMap = {}
   
def updateItemMap(item, itemMap):
  keys = itemMap.keys()
  number = len(keys)
  if(number == 0):
    itemMap[1] = item
  else:
    maxKey = keys[len(keys)-1]     
    findFlag = False
    for key in keys:
        #start the process of tracing
        overlap = computerOverlap(item, itemMap[key])
        area1 = computeArea(itemMap[key])
        area2 = computeArea(item)
        ratio = overlap*1.0/(area1+area2-overlap) # Compute the ratio of lap area
        #print(str(item)+"and"+str(itemMap[key])+"="+str(ratio))
        if(ratio > 0.6):
           itemMap[key] = item # update itemMap which always store the newest frame tracked
           itemMap[key].findFlag = 1 
           findFlag = True # show that find the similar item
           break     
    if(findFlag == False):       
        itemMap[maxKey+1] = item # if the position of this item in the newest frame didn't show in the last frame, suggest that this item presents just now, so need to run itemMap[maxKey+1] = item to add item into the new element
  return itemMap      

def clearTracing(itemMap):  
    for key in itemMap.keys():
       if(itemMap[key].stateFlag == 2):
         itemMap.pop(key)
    return itemMap
def clearFindflag(itemMap):  
    for key in itemMap.keys():
        itemMap[key].findFlag = 0
    return itemMap  
def refreshStateflag(itemMap):  
    for key in itemMap.keys():
        if(itemMap[key].findFlag == 0 and itemMap[key].stateFlag == 1):# 
           itemMap[key].stateFlag = 2
        if(itemMap[key].findFlag == 1 and itemMap[key].stateFlag == 0):
           itemMap[key].stateFlag = 1
    return itemMap


def updateItemList(list):
    for i in range(len(list)):
        find = False
        tempItem = Item(list[i][0], list[i][1], list[i][2], list[i][3])
        max_ratio = 0
        location = -1
        area2 = computeArea(tempItem)
        for j in range(len(itemList)):
            overlap = computerOverlap(tempItem, itemList[j])
            area1 = computeArea(itemList[j])
            ratio = overlap*1.0/(area1+area2-overlap)
            if(ratio > 0.6 and ratio > max_ratio):
                max_ratio = ratio
                location = j
        if max_ratio != 0 and location != -1:
            itemList[location].xmin = tempItem.xmin
            itemList[location].xmax = tempItem.xmax
            itemList[location].ymin = tempItem.ymin
            itemList[location].ymax = tempItem.ymax
            itemList[location].findFlag = 1
            itemList[location].centers.append(((tempItem.xmin+tempItem.xmax)/2, (tempItem.ymin+tempItem.ymax)/2))
            find = True
        if find == False:
            tempItem.findFlag = 1
            #num[0] += 1
            #tempItem.num = num[0]
            tempItem.isNew = True
            itemList.append(tempItem)
    length = len(itemList)
    index = 0
    #removeNum = 0
    while index < length:
        if itemList[index].findFlag == 0:
            itemList.remove(itemList[index])
            #removeNum += 1
            index -= 1
            length -= 1
        index += 1
    #num[0] -= removeNum
    for i in range(len(itemList)):
        itemList[i].findFlag = 0
        #if itemList[i].isNew == True:
            #itemList[i].num -= removeNum