# -*- coding: utf8 -*-

import numpy as np  
import matplotlib.pyplot as plt
from scipy import optimize  
  
# register the data of trace into two arrays x, y
def Generate_x_y_arry(trace_coordinate): 
    x_list = []
    y_list = []
    #txt = '20170806130001	1	0.92	[(220, 745), (202, 756), (196, 757), (185, 761), (172, 764), (154, 768), (148, 771), (148, 777), (143, 778), (141, 780), (138, 783), (136, 786), (123, 792), (115, 796), (112, 797), (109, 795), (101, 792), (95, 797), (93, 796), (89, 796), (81, 798), (69, 801), (63, 804)]'
    line_info = trace_coordinate.split('\t',3)
    result = line_info[3].strip('[]')
    result = result.replace(' ','')
    result = result.replace('(','')
    result = result.replace(')','')
    item = result.split(',')
    for i in range(len(item)):
        if i%2 == 0 :
            int_item = int(item[i])
            x_list.append(int_item)
        else :
            y_list.append(int_item)
    x = np.array(x_list)
    y = np.array(y_list)
    trace_time = line_info[0]
    id_of_lane = line_info[1] 
    return trace_time, id_of_lane, x, y  
  
# fit the trace using 3 polynomial
def Fit_trace_curve(x,y):  
    f1 = np.polyfit(x, y, 3)  
    p2 = np.poly1d(f1)  
    # print(p2)    
    yvals = p2(x)  #fiy y,also can use yvals=np.polyval(f1, x)
    return f1, yvals 

# draw trace figure
def Draw_trace_curve(x,y,y1):
    plot1 = plt.plot(x, y, 's',label='original values')  
    plot2 = plt.plot(x, y1, 'r',label='polyfit values')  
    plt.xlabel('x')  
    plt.ylabel('y')  
    plt.legend(loc=4) #assigh the lower right corner of lengend
    plt.title('polyfitting')  
    plt.show()  
    plt.savefig('test.png')

#define line formulation
def Line_func(x, A, B):
    return A*x + B

#fit vehicle line
def Fit_line(ix,iy,cx,cy):
    xlist = []
    ylist = []
    xlist.append(ix)
    xlist.append(cx)
    ylist.append(iy)
    ylist.append(cy)
    A, B = optimize.curve_fit(Line_func, xlist, ylist)[0]
    p1 = np.poly1d([A, B])
    return A, B

# filter points which are not satisfied the range
def filter_point(temp_obj,xmin,xmax,ymin,ymax):
    point_x = temp_obj.coordinate_x
    point_y = temp_obj.coordinate_y
    x = []
    y = []
    for i in range(len(point_x)):
        if (point_x[i] <= xmax) & (point_x[i] >= xmin):
            if (point_y[i] <= ymax) & (point_y[i] >= ymin):
                x.append(point_x[i])
                y.append(point_y[i])
    # print x
    # print y
    # print "******************"
    return x,y


# judge the position of the trace point comparing to the vehicle line
def Judge_position(temp_obj, A, B, xmin, xmax, ymin, ymax):
    point_x = temp_obj.coordinate_x
    point_y = temp_obj.coordinate_y

    # filter the datum which are not meet the range 
    new_x, new_y = filter_point(temp_obj,xmin,xmax,ymin,ymax)
    flag = False
    if (len(new_x) != 0):
        left = 0
        right = 0
        online = 0
        for i in range(len(new_x)):
            value = A * new_x[i] + B - new_y[i]
            if value > 0:
                left = left + 1
            elif value < 0:
                right = right + 1
            else :
                online = online + 1
        if (left != 0) & (right != 0):
            flag = True 
            print "C_L_Y_X: ", i
            print "ID_LANE: ", temp_obj.id_of_lane
            print "TIME: ", temp_obj.track_time
    return flag


    #do not judge the range of x,y
    # left = 0
    # right = 0
    # online = 0
    # flag = False
    # for i in range(len(point_x)):
    #     value = A * point_x[i] + B - point_y[i]
    #     if value > 0:
    #         left = left + 1
    #     elif value < 0:
    #         right = right + 1
    #     else :
    #         online = online + 1
    # if (left != 0) & (right != 0):
    #     flag = True 
    #     print "C_L_Y_X: ", i
    #     print "ID_LANE: ", temp_obj.id_of_lane
    #     print "TIME: ", temp_obj.track_time
    # return flag

    #judge the range of x,y
    # left = []
    # right = []
    # online = []
    # flag = False
    # for i in range(len(point_x)):
    #     value = A * point_x[i] + B - point_y[i]
    #     if value > 0:
    #         left.append([point_x[i],point_y[i]])
    #     elif value < 0 :
    #         right.append([point_x[i],point_y[i]])
    #     else :
    #         online.append([point_x[i],point_y[i]]) 
    
    # if (len(left) != 0) & (len(right) != 0) :
    #     if len(left) >= len(right):
    #         for i in range(len(right)):
    #             x = right[i][0]
    #             y = right[i][1]
    #             if (x <= xmax) & (x >= xmin):
    #                 if (y <= ymax) & (y >= ymin):
    #                     flag = True 
    #                     print "C_L_Y_X: ", i
    #                     print "ID_LANE: ", temp_obj.id_of_lane
    #                     print "TIME: ", temp_obj.track_time
    #     else:
    #         for i in range(len(left)):
    #             x = left[i][0]
    #             y = left[i][1]
    #             if (x <= xmax) & (x >= xmin):
    #                 if (y <= ymax) & (y >= ymin):
    #                     flag = True 
    #                     print "C_L_Y_X: ", i
    #                     print "ID_LANE: ", temp_obj.id_of_lane
    #                     print "TIME: ", temp_obj.track_time
    # return flag



