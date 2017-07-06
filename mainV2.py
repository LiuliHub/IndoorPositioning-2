#!/usr/bin/python
# -*- coding: utf-8 -*-

from img import *
from src.frameV2 import *
import sys
import time

if len(sys.argv) >= 2:
	frame_img = sys.argv[1]
else:
	print "No està especificat el nom de la imatge"
	sys.exit(0)
frame = Frame()
frame.ReadFrame(frame_img, 90)
frame.save_th()
time1 = time.time()
frame.GetPuzzleCircles()
print("--- %s seconds ---" % (time.time() - time1))
for info in frame.CirclesInfo:
   frame.DrawInImage(info,3)  
print "Hi han "+str(frame.Centers)
line = frame.GetLinedPoints()
OrderPoints =  frame.GetoOrderPoints(line)
Points =[frame.Centers[OrderPoints[0] - 1], frame.Centers[OrderPoints[1]- 1], frame.Centers[OrderPoints[2]- 1], frame.Centers[OrderPoints[3]- 1]]
print "Index centre ordenats: "+str(OrderPoints)
print "Centres ordenats: "+str(Points)
Points_filtered=frame.CheckCenters(Points)
print"Centres filtrats: "+str(Points_filtered)
frame.DrawInImage(Points_filtered,2)
frame.save()
