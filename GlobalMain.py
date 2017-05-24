#!/usr/bin/python
# -*- coding: utf-8 -*-

from img import *
from frameV2 import *
from calculate_coordinates import *
import sys
import time
import numpy as np
import picamera
'''
picamera.PiResolution(2592, 1944)
camera = picamera.PiCamera()
camera.capture('img.jpg')
'''
frame = Frame()
frame.ReadFrame("./test9950_O.jpg", 70)
time1 = time.time()
frame.GetPuzzleCircles()
frame.DrawInImage(frame.Centers,5)
#frame.save()
print("--- %s seconds ---" % (time.time() - time1))
line = frame.GetLinedPoints()
def distance(Pi,Pj):
    return np.sqrt( np.abs(Pi[0]-Pj[0])**2.0 + np.abs(Pi[1]-Pj[1])**2.0 + np.abs(Pi[2]-Pj[2])**2.0 )
P1 = [0,0,0]
P2 = [0,100,0]
P4 = [40,0,0]
P3 = [40,100,0]

s12 = distance(P1,P2)
s13 = distance(P1,P3)
s14 = distance(P1,P4)
s23 = distance(P2,P3)
s24 = distance(P2,P4)
s34 = distance(P3,P4)

E = Enviroment3d(s12,s13,s14,s23,s24,s34)

OrderPoints =  frame.GetoOrderPoints(line)
Points =[frame.Centers[OrderPoints[0] - 1], frame.Centers[OrderPoints[1]- 1], frame.Centers[OrderPoints[2]- 1], frame.Centers[OrderPoints[3]- 1]]
result = E.Pixel2Camera(Points)
E.AddPointsTest(result)

print "-------- Distance found --------"
print "Focal Length: "+str(E.FindF())
print "Distance 1: "+str(E.d1())
print "Distance 2: "+str(E.d2())
print "Distance 3: "+str(E.d3())
print "Distance 4: "+str(E.d4())
print "**********************************"
