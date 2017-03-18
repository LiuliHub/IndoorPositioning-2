#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import sys
import time

if len(sys.argv) >= 2:
	frame_img = sys.argv[1]
else:
	print "No està especificat el nom de la imatge"
	sys.exit(0)

# Load an color image in grayscale
img = cv2.imread(frame_img,0)
# Convert to BW 0=white, 255=black (?)
(thresh, im_bw) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

xdim=im_bw.shape[0]
ydim=im_bw.shape[1]

for ix in range(xdim):
   ww=np.where(im_bw[ix,0:ydim]==0)[0]  # where returns a tuple...Why?? -> get first element
   if len(ww) > 0:
       # Trobar grups de coses http://stackoverflow.com/questions/7352684/how-to-find-the-groups-of-consecutive-elements-from-an-array-in-numpy
       wwsplit = np.split(ww,  np.where(np.diff(ww)!=1)[0] )
       print("Aquí : "+str(ix)+" hi ha "+str(len(wwsplit))+" coses")
       
       img[ix,:]+=10  # Mark image row
       
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

