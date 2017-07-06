#!/usr/bin/python
# -*- coding: utf-8 -*-

from img import *
from src.frameV2 import *
from src.calculate_coordinates import *
import sys
import time
import numpy as np

if len(sys.argv) >= 2:
	frame_img = sys.argv[1]
else:
	print "No està especificat el nom de la imatge"
	sys.exit(0)
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

frame = Frame()
frame.ReadFrame(frame_img, 85)
time1 = time.time()
frame.save_th()

frame.GetPuzzleCircles()

print("--- %s seconds ---" % (time.time() - time1))
line = frame.GetLinedPoints()

E = Enviroment3d(s12,s13,s14,s23,s24,s34)

OrderPoints =  frame.GetoOrderPoints(line)
Points =[frame.Centers[OrderPoints[0] - 1], frame.Centers[OrderPoints[1]- 1], frame.Centers[OrderPoints[2]- 1], frame.Centers[OrderPoints[3]- 1]]
print (frame.Centers)
print(Points)
Points_filtered=frame.CheckCenters(Points)
frame.DrawInImage(frame.Centers,5)
frame.save()
print(Points_filtered)
result = E.Pixel2Camera(Points_filtered)
E.AddPointsTest(result)
#E.Tmatrix(result[0], result[1], result[2], result[3])
#XYZ = E.GetPositonXYZ()
print "-------- Distance found --------"
print "Distance 1: "+str(E.d1())
print "Distance 2: "+str(E.d2())+""
print "Distance 3: "+str(E.d3())
print "Distance 4: "+str(E.d4())
#print "Xo:"+str(XYZ[0])+"	Yo:"+str(XYZ[1])+"	Zo:"+str(XYZ[2])
#print "a:"+str(XYZ[3])+"	b:"+str(XYZ[4])+"	c:"+str(XYZ[5])
print "**********************************"
