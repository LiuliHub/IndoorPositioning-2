#!/usr/bin/python
# -*- coding: utf-8 -*-

from img import *
from frame import *
import sys

if len(sys.argv) >= 2:
	frame_img = sys.argv[1]
else:
	print "No està especificat el nom de la imatge"
	sys.exit(0)

frame = Frame()
frame.ReadFrame(frame_img)
'''
pixels=[]
for i in range(0,200):
    pixels.append([300,0+i])
frame.DrawInImage(pixels,10)
'''
#frame.save()
pixels = frame.GetPuzzleCircles()
pixels_a = []
for i in pixels:
	for j in i:
		pixels_a.append(j)
		#print str(j[0])+" ,"+str(j[1])

print str(len(pixels_a))
frame.DrawInImage(pixels_a,1)
frame.save()
