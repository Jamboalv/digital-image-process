#-*- coding: utf8 -*-

import sys,os
import cv2

kilobytes = 1024
megabytes = kilobytes*1024
chunksize = int(30*megabytes)
# cap = cv2.VideoCapture("VIDEO PATH")
# fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
# size = (int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

def split(fromfile,todir,chunksize=chunksize):
    if not os.path.exists(todir):
        os.mkdir(todir) 
    else:
        for fname in os.listdir(todir):
            os.remove(os.path.join(todir,fname))
    partnum = 0
    inputfile = open(fromfile,"rb")
    while True:
        chunk = inputfile.read(chunksize)
        if not chunk:
            break
        partnum = partnum + 1
        filename = os.path.join(todir, ("abc%04d"%partnum))
        print("the filename you want to show："+filename)
        fileobj = open(filename, "wb")
        fileobj.write(chunk)
        #cv2.VideoWriter(filename+'.mpg',cv2.cv.CV_FOURCC('M','J','P','G'),fps,size).write(chunk)
        fileobj.close()
    inputfile.close()
    assert partnum <= 9999
    return partnum

if __name__=="__main__":
    fromfile = "./VIDEO NAME"     
    todir = "./split/"
    #chunksize = int(5000000)
    absfrom,absto = map(os.path.abspath,[fromfile,todir])
    #print("分割：",absfrom,‘to‘,absto,‘by‘,chunksize)
    try:
        parts = split(fromfile,todir,chunksize)
    except:
        print("Error during split:")
        print(sys.exc_info()[0],sys.exc_info()[1])
    else:
        print("FINISHED:",parts,"parts are in",absto)


