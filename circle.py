#!/usr/bin/python
# -*- coding: utf-8 -*-

# Library imports
from img import *
from random import randrange

#Class Circles
class Circles(object):
    def __init__(self, PixelPuzzle, X_Pixels, Y_Pixels):
        self.Circles = []
        self.X_Pixels = X_Pixels
        self.Y_Pixels = Y_Pixels
        self.PixelPuzzle = PixelPuzzle

    def GetFigures(self):
        # keep looking till you find 4 bloobs
        while (len(self.Circles) < 4):
            RandomPixel =  self.PixelPuzzle[randrange(len(self.PixelPuzzle))]
            # Get the margin of the random black pixel
            XTop = self.FindXTop(RandomPixel)
            XDown = self.FindXDown(RandomPixel)
            YRight = self.FindYRight(RandomPixel)
            YLeft= self.FindYLeft(RandomPixel)
            center = [self.GetMiddlePoint(XTop,XDown)[0], self.GetMiddlePoint(YRight,YLeft)[1]]
            if(self.IsValidCenter(center)):
                self.Circles.append(center)

                
    def FindXTop(self, RandomPixel):
        YPositionPixel = RandomPixel[1]
        XPositionPixel = RandomPixel[0]
        for i in range(0, XPositionPixel):
            if [XPositionPixel - i,YPositionPixel] not in self.PixelPuzzle:
                return [XPositionPixel - i,YPositionPixel]

    def FindXDown(self, RandomPixel):
        YPositionPixel = RandomPixel[1]
        XPositionPixel = RandomPixel[0]
        for i in range(XPositionPixel, self.X_Pixels):
            if [i,YPositionPixel] not in self.PixelPuzzle:
                return [i,YPositionPixel]

    def FindYRight(self, RandomPixel):
        XPositionPixel = RandomPixel[0]
        YPositionPixel = RandomPixel[1]
        for i in range(YPositionPixel, self.Y_Pixels):
            if [XPositionPixel,i] not in self.PixelPuzzle:
                return [XPositionPixel,i]

    def FindYLeft(self, RandomPixel):
        XPositionPixel = RandomPixel[0]
        YPositionPixel = RandomPixel[1]
        for i in range(0, YPositionPixel):
            if [XPositionPixel, YPositionPixel -i] not in self.PixelPuzzle:
                return [XPositionPixel, YPositionPixel -i]

    def GetMiddlePoint(self, pixel1, pixel2):
        XMiddle = abs((pixel1[0] + pixel2[0])/2)
        YMiddle = abs((pixel1[1] + pixel2[1])/2)
        return [XMiddle,YMiddle]

    def IsValidCenter(self, center):
        ValidCenter = True                
        for i in self.Circles:
            XDifference = abs(i[0] - center[0])
            YDifference = abs(i[1] - center[1])
            if (((XDifference+YDifference)/2) < 50):
                ValidCenter = False
                return ValidCenter
        return ValidCenter
        
        


    def GetCircles(self,PixelPuzzle ):  
        return 0  
    def GetCenter(self):
        return 0