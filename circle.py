#!/usr/bin/python
# -*- coding: utf-8 -*-

# Library imports
from random import randrange
import time

#Class Circles
class Circles(object):
    def __init__(self, PixelPuzzle, X_Pixels, Y_Pixels):
        self.CirclesCenters = []
        self.X_Pixels = X_Pixels
        self.Y_Pixels = Y_Pixels
        self.PixelPuzzle = PixelPuzzle

    def GetFigures(self):
        NewCircle = True
        # keep looking till you find 4 bloobs
        while (len(self.CirclesCenters) < 4):
            if(NewCircle):
                #If it's the first time we track a new circle we will pick a random point
                Point =  self.PixelPuzzle[randrange(len(self.PixelPuzzle))]
                time1 = time.time()                    
            else:
                #If we didn't find the center the first time we will try to find it 
                #again now with the reference of the provious fake center
                Point = center
            # Get the margin of the random black pixel
            XTop = self.FindXTop(Point)
            XDown = self.FindXDown(Point)
            YRight = self.FindYRight(Point)
            YLeft= self.FindYLeft(Point)
            center = [self.GetMiddlePoint(XTop,XDown)[0], self.GetMiddlePoint(YRight,YLeft)[1]]
            if(self.IsValidCenter(center, Point)):
                NewCircle = True
                if(self.IsAlreadyACenter(center)):
                    self.CirclesCenters.append(center)
                    print("--- %s seconds ---" % (time.time() - time1)) 
                    print "Hi han "+str(center)
                    #time1 = time.time()            
                                                            
            else:
                NewCircle = False                   
    def FindXTop(self, Point):
        YPositionPixel = Point[1]
        XPositionPixel = Point[0]
        for i in range(0, XPositionPixel):
            if [XPositionPixel - i,YPositionPixel] not in self.PixelPuzzle:
                return [XPositionPixel - i,YPositionPixel]

    def FindXDown(self, Point):
        YPositionPixel = Point[1]
        XPositionPixel = Point[0]
        for i in range(XPositionPixel, self.X_Pixels):
            if [i,YPositionPixel] not in self.PixelPuzzle:
                return [i,YPositionPixel]

    def FindYRight(self, Point):
        XPositionPixel = Point[0]
        YPositionPixel = Point[1]
        for i in range(YPositionPixel, self.Y_Pixels):
            if [XPositionPixel,i] not in self.PixelPuzzle:
                return [XPositionPixel,i]

    def FindYLeft(self, Point):
        XPositionPixel = Point[0]
        YPositionPixel = Point[1]
        for i in range(0, YPositionPixel):
            if [XPositionPixel, YPositionPixel -i] not in self.PixelPuzzle:
                return [XPositionPixel, YPositionPixel -i]

    def GetMiddlePoint(self, pixel1, pixel2):
        XMiddle = abs((pixel1[0] + pixel2[0])/2)
        YMiddle = abs((pixel1[1] + pixel2[1])/2)
        return [XMiddle,YMiddle]
    
    def IsValidCenter(self, center, point):
        XDifference = abs(point[0] - center[0])
        YDifference = abs(point[1] - center[1])
        if (((XDifference+YDifference)/2) < 2):
            return True
        return False

    def IsAlreadyACenter(self, center):
        ValidCenter = True                
        for i in self.CirclesCenters:
            XDifference = abs(i[0] - center[0])
            YDifference = abs(i[1] - center[1])
            if (((XDifference+YDifference)/2) < 50):
                ValidCenter = False
                return ValidCenter
        return ValidCenter

    def GetCenters(self):
        return self.CirclesCenters
