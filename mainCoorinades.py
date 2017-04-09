#!/usr/bin/python
# -*- coding: utf-8 -*-

from calculate_coordinates import *

s12 = 77.5
s13 = 177.5
s14 = 162
s23 = 160
s24 = 191.5
s34 = 104.5

E = Enviroment3d(s12,s13,s14,s23,s24,s34)
E.AddPointsPicture(-2.214,-0.934)
E.AddPointsPicture(-2.564,1.420)
E.AddPointsPicture(2.442,1.948)
E.AddPointsPicture(2.657,-1.143)
print E.A1()

