#!/usr/bin/python
# -*- coding: utf-8 -*-

from img import *
from frameV2 import *
import sys
import time

if len(sys.argv) >= 2:
	frame_img = sys.argv[1]
else:
	print "No està especificat el nom de la imatge"
	sys.exit(0)
frame = Frame()
frame.ReadFrame(frame_img, 70)
#frame.save_th()
time1 = time.time()
frame.GetPuzzleCircles()
print("--- %s seconds ---" % (time.time() - time1))
'''
for info in frame.CirclesInfo:
   frame.DrawInImage(info,10)  
   '''
frame.DrawInImage(frame.Centers,5)
frame.save()
print "Hi han "+str(frame.Centers)
print "Hi han "+str(len(frame.CirclesInfo))

