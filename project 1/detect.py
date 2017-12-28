# -*- coding: utf8 -*-

import argparse      
import time  
import numpy as np 
import os
import random
import math
import sys
import matplotlib.pyplot as plt
from scipy import optimize  
from scipy.optimize import fsolve
from fit_line import *

class Vehicle:
    def __init__(self, track_time, id_of_lane,):
        self.track_time = track_time
        self.id_of_lane = id_of_lane
        self.coordinate_x = []
        self.coordinate_y = []
        self.coordinate_yvals = []

global p1,f2, A, B

def fx(xy):
    x = float(xy[0])
    y = float(xy[1])
    return [
            f2[0] * x**3 + f2[1] * x**2 + f2[2] * x + f2[3] - y ,
            A * x + B -y 
    ]

def detect_press_line(txt,ix,iy,cx,cy):
    All_Record = txt.readlines()

    xmin = min([ix,cx])
    xmax = max([ix,cx])
    ymin = min([iy,cy])
    ymax = max([iy,cy])

    A,B = Fit_line(ix,iy,cx,cy)

    Vehicle_obj_list = []

    for line in All_Record:
        temp_time, temp_id, tempx, tempy = Generate_x_y_arry(line)
        tem_Vehicle_obj = Vehicle(temp_time,temp_id)
        tem_Vehicle_obj.coordinate_x = tempx
        tem_Vehicle_obj.coordinate_y = tempy
        Vehicle_obj_list.append(tem_Vehicle_obj)
    
    press_line_num = 0                                                                                                                                                                      
    
    j = 0
    while (j < len(Vehicle_obj_list)):
    #for i in range(len(Vehicle_obj_list)):
        temp_obj = Vehicle_obj_list[j]

        flag = Judge_position(temp_obj,A,B,xmin,xmax,ymin,ymax)
        if flag == True :
            press_line_num = press_line_num + 1
        j = j + 1

        # f2, temp_yvals = Fit_trace_curve(temp_obj.coordinate_x, temp_obj.coordinate_y)
        # temp_obj.coordinate_yvals = temp_yvals
        # result = fsolve(fx,[0,0]) 
        # error = fx(result)
        # if error[0] == error[1]:
        #     if (result[0] <= xmax) & (result[0] >= xmin) :
        #         if (result[1] <= ymax) & (result[1] >= ymin) :
        #             print "C_L_Y_X: ", i
        #             print "ID_LANE: ", temp_obj.id_of_lane
        #             print "TIME: ", temp_obj.track_time
        #             press_line_num = press_line_num + 1
    if press_line_num != 0:
        print press_line_num  
 





    


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    

    