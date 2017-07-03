#!/usr/bin/python                                                                                      
# -*- coding: utf-8 -*-                                                                                

from img import *
from frameV2 import *
from calculate_coordinates import *
import sys
import time
import numpy as np
import picamera
camera = picamera.PiCamera()
camera.resolution = (512,384)
camera.rotation = 180
def distance(Pi,Pj):
    return np.sqrt( np.abs(Pi[0]-Pj[0])**2.0 + np.abs(Pi[1]-Pj[1])**2.0 + np.abs(Pi[2]-Pj[2])**2.0 )
P1 = [0,0,0]
P4 = [0,100,0]
P2 = [40,0,0]
P3 = [40,100,0]
s12 = distance(P1,P2)
s13 = distance(P1,P3)
s14 = distance(P1,P4)
s23 = distance(P2,P3)
s24 = distance(P2,P4)
s34 = distance(P3,P4)
while(True):
    frame = Frame()
    E = Enviroment3d(s12,s13,s14,s23,s24,s34)
    time1 = time.time()
    camera.capture('img.jpg')
    frame.ReadFrame("./img.jpg", 80)
    
    frame.GetPuzzleCircles()
    
    time2 = time.time()
    print frame.Centers
    line = frame.GetLinedPoints()
    OrderPoints =  frame.GetoOrderPoints(line)
    Points =[frame.Centers[OrderPoints[0] - 1], frame.Centers[OrderPoints[1]- 1], frame.Centers[OrderPoints[2]- 1], frame.Centers[OrderPoints[3]- 1]]
    Points_filtered=frame.CheckCenters(Points)
    #frame.DrawInImage(Points_filtered,5)
    frame.save()
    print Points
    print Points_filtered
    result = E.Pixel2Camera(Points)
    E.AddPointsTest(result)
    E.Tmatrix(P1,P2,P3,P4)
    XYZ = E.GetPositonXYZ()
    print("--- %s seconds ---" % (time2 - time1))
    print "-------- Distance found --------"
    print "Distance 1: "+str(E.d1())
    print "Distance 2: "+str(E.d2())+""
    print "Distance 3: "+str(E.d3())
    print "Distance 4: "+str(E.d4())
    print "X0 = "+str(XYZ[0])
    print "Y0 = "+str(XYZ[1])
    print "Z0 = "+str(XYZ[2])
    print "a = "+str(np.rad2deg(XYZ[3]))
    print "b = "+str(np.rad2deg(XYZ[4]))
    print "c = "+str(np.rad2deg(XYZ[5]))
    
    print "********************************"


    
