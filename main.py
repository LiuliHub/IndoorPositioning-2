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
pixels=[]
for i in range(0,500):
    pixels.append([0,0+i])
frame.DrawInImage(pixels)
frame.save()

