#!/usr/bin/python
# -*- coding: utf-8 -*-

from calculate_coordinates import *
import time
import numpy as np

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
'''
# Points ~ 880 distance
Points = [[597,1460], [609,1748],[723,1744],[711,1456]]
# Points ~ 680 distance
Points = [[769,1256],[786,1630],[938,1624],[917,1248]]
# Points ~ 9950 Original distance
Points = [ [74, 1489], [39, 1756], [151, 1751],[180, 1486]]
# Points ~ 9950 R distance
Points = [[35, 735], [19, 866], [74, 864], [89, 734]]
# Points  distance
Points = [[699, 2005], [706, 2225], [791, 2221], [782, 2001] ]
'''
# Points ~ 9950 R distance
Points = [[35, 735], [19, 866], [74, 864], [89, 734]]
result = E.Pixel2Camera(Points)
E.AddPointsTest(result)

print "-------- Distance found --------"
print "Focal Length: "+str(E.FindF())
print "Distance 1: "+str(E.d1())
print "Distance 2: "+str(E.d2())
print "Distance 3: "+str(E.d3())
print "Distance 4: "+str(E.d4())
print "**********************************"



