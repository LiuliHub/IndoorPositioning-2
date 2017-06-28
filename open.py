#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import sys
import numpy as np;
import time

if len(sys.argv) >= 2:
	frame_img = sys.argv[1]
else:
	print "No està especificat el nom de la imatge"
	sys.exit(0)

im = cv2.imread(frame_img, cv2.IMREAD_GRAYSCALE)
 
# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector()

time1 = time.time() 
# Detect blobs.
keypoints = detector.detect(im)
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
print("--- %s seconds ---" % (time.time() - time1))
 
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)