#!/usr/bin/python
# -*- coding: utf-8 -*-

from calculate_coordinates import *
import time

s12 = 93.6
s13 = 122.1
s14 = 62.5
s23 = 50.0
s24 = 90.0
s34 = 89.4

E = Enviroment3d(s12,s13,s14,s23,s24,s34)
E.AddPointsPicture(-4.01,5.82)
E.AddPointsPicture(-2.890,5.125)
E.AddPointsPicture(-3.019,4.514)
E.AddPointsPicture(-4.132,4.979)
time1 = time.time()
print E.FindF()
print E.d1()
print E.d2()
print E.d3()
print E.d4()
print("--- %s seconds ---" % (time.time() - time1))
