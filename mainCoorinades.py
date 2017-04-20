#!/usr/bin/python
# -*- coding: utf-8 -*-

from calculate_coordinates import *
import time
import numpy as np


def distance(Pi,Pj):
    return np.sqrt( np.abs(Pi[0]-Pj[0])**2.0 + np.abs(Pi[1]-Pj[1])**2.0 + np.abs(Pi[2]-Pj[2])**2.0 )
P4 = [0,0,0]
P3 = [0,150,0]
P1 = [150,0,0]
P2 = [150,150,0]

s12 = distance(P1,P2)
s13 = distance(P1,P3)
s14 = distance(P1,P4)
s23 = distance(P2,P3)
s24 = distance(P2,P4)
s34 = distance(P3,P4)


E = Enviroment3d(s12,s13,s14,s23,s24,s34)
P1c = E.World2Camera(P1)
Q1 = E.Camera2Picture(P1c)
P2c = E.World2Camera(P2)
Q2 = E.Camera2Picture(P2c)
P3c = E.World2Camera(P3)
Q3 = E.Camera2Picture(P3c)
P4c = E.World2Camera(P4)
Q4 = E.Camera2Picture(P4c)
E.AddPointsPicture(Q1[0][0][0],Q1[1][0][0])
E.AddPointsPicture(Q2[0][0][0],Q2[1][0][0])
E.AddPointsPicture(Q3[0][0][0],Q3[1][0][0])
E.AddPointsPicture(Q4[0][0][0],Q4[1][0][0])
print "**********************************"
print "-------- Distance real --------"
print "Distance 1: "+str(distance(P1,E.CameraCenterPrint))
print "Distance 2: "+str(distance(P2,E.CameraCenterPrint))
print "Distance 3: "+str(distance(P3,E.CameraCenterPrint))
print "Distance 4: "+str(distance(P4,E.CameraCenterPrint))

print "-------- Distance found --------"
print "Focal Length: "+str(E.FindF())
print "Distance 1: "+str(E.d1())
print "Distance 2: "+str(E.d2())
print "Distance 3: "+str(E.d3())
print "Distance 4: "+str(E.d4())
print "**********************************"

