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
time1 = time.time()
for ix in range(xdim):
   # Search black parts in each line
   ww=np.where(im_bw[ix,0:ydim]==0)[0]  # where returns a tuple...Why?? -> get first element
   if len(ww) > 0:
       # Trobar grups de coses...
       wwsplit = np.split(ww,  np.where(np.diff(ww)!=1)[0] )
       #print("Aquí : %d hi ha %d coses") % (ix, len(wwsplit))
       
       for il in range(len(wwsplit)):
          # Find the mean value
          if (wwsplit[il] != []):
            cx = np.floor(np.mean(wwsplit[il])).astype(np.int)
            # Find the points in the column
            xx=np.where(im_bw[:,cx]==0)[0]
            # Split column into parts
            xxsplit = np.split(xx,  np.where(np.diff(xx)!=1)[0] )
            
            for ik in range( len(xxsplit)):
                if np.sum(xxsplit[ik]==ix)>0:
                    cy = np.floor(np.mean(xxsplit[ik])).astype(np.int)
                    #print "Posició %d , %d " % (cx,cy)
                    cv2.circle(img, (cx,cy), 10, 255, thickness=1, lineType=8, shift=0)
       img[ix,:]+=10  # Mark image row
print("--- %s seconds ---" % (time.time() - time1))       
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

