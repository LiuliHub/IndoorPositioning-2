#!/usr/bin/python
# -*- coding: utf-8 -*-

# Library imports
from img import *
from PIL import Image, ImageFilter
import time


class Frame(object):
    def __init__(self):
        self.PixelMap = []
        self.Centers = []
        self.CirclesInfo = []
        self.OriginalMap = []


    def GetFrameInfo(self):
        return [len(self.PixelMap),len(self.PixelMap[0])]
    def ReadFrame(self, FileName, thresh):
        image = Image.open(FileName)
        OriginalPix = image.load()
        OX, OY = image.size[0], image.size[1] 
        image = image.point(lambda i: 255 if i > thresh else 0)
        pix = image.load()
        X, Y = image.size[0], image.size[1]
        data = [[pix[x,y] for x in range(X)] for y in range(Y)]        
        OriginalData = [[OriginalPix[x,y] for x in range(OX)] for y in range(OY)] 
        self.PixelMap = data
        self.OriginalMap = OriginalData  

    def save(self):
        i = img(self.OriginalMap,'RGB')
        image = Image.new(format(i),(get_w(i),get_h(i)))
        image.putdata([pixel for F in matrix(i) for pixel in F])
        fn = "./Img/%i.jpg" % int(time.time())
        image.save(fn)
    def save_th(self):
        i = img(self.PixelMap,'RGB')
        image = Image.new(format(i),(get_w(i),get_h(i)))
        image.putdata([pixel for F in matrix(i) for pixel in F])
        fn = "./Img/%i.jpg" % int(time.time())
        image.save(fn)

    def DrawInImage(self,ArrayPixels,thickness):
        matrix = self.OriginalMap
        for pixel in ArrayPixels:
            if(thickness == 1):
                self.OriginalMap[pixel[0]][pixel[1]] = (0,255,0)
            else:
                for i in range(0, thickness):
                    self.OriginalMap[pixel[0]+i][pixel[1]] = (0,255,0) 

        return 0

    def WitchColorPixel(self, Pixel):
        if((Pixel[0]<10)&(Pixel[1]<10)&(Pixel[2]<10)):
           #print "Black"
            return 1
        else:
             #print "White"
            return 0
                              

    def GetPuzzleCircles(self):
        for x in range(len(self.PixelMap)):
            for y in range(len(self.PixelMap[x])):
                    #Check if it's black
                if (self.WitchColorPixel(self.PixelMap[x][y]) == 1):
                    #Check if pixel already in a circle existing
                    if (self.NotIn([x,y])):
                        self.SearchCircleInfo([x,y],[])
                        if(len(self.Centers) == 5):
                            return 0

        return 0

    def SearchCircleInfo(self, Point, Info):
        XTop = self.FindXTop(Point)
        XDown = self.FindXDown(Point)
        YRight = self.FindYRight(Point)
        YLeft= self.FindYLeft(Point)
        #Update Circle Info
        if (Info == []):
            Info = [XTop,XDown,YRight,YLeft]
        else:
            if Info[0][0] > XTop[0]:
                Info[0] = XTop
            if Info[1][0] < XDown[0]:
                Info[1] = XDown
            if Info[2][1] < YRight[1]:
                Info[2] = YRight
            if Info[3][1] > YLeft[1]:
                Info[3] = YLeft
        center = [self.GetMiddlePoint(XTop,XDown)[0], self.GetMiddlePoint(YRight,YLeft)[1]]
        if(self.IsValidCenter(center, Point)):
            self.CheckCenter(center, Info)
        else:
            self.SearchCircleInfo(center, Info)
        
    def FindXTop(self, Point):
        YPositionPixel = Point[1]
        XPositionPixel = Point[0]
        for i in range(0, XPositionPixel):
            if self.WitchColorPixel(self.PixelMap[XPositionPixel - i][YPositionPixel]) == 0:
                return [XPositionPixel - i,YPositionPixel]

    def FindXDown(self, Point):
        YPositionPixel = Point[1]
        XPositionPixel = Point[0]
        for i in range(XPositionPixel, len(self.PixelMap)):
            if self.WitchColorPixel(self.PixelMap[i][YPositionPixel]) == 0:
                return [i,YPositionPixel]

    def FindYRight(self, Point):
        XPositionPixel = Point[0]
        YPositionPixel = Point[1]
        for i in range(YPositionPixel, len(self.PixelMap[0])):
            if self.WitchColorPixel(self.PixelMap[XPositionPixel][i]) == 0:
                return [XPositionPixel,i]

    def FindYLeft(self, Point):
        XPositionPixel = Point[0]
        YPositionPixel = Point[1]
        for i in range(0, len(self.PixelMap[0])):
            if self.WitchColorPixel(self.PixelMap[XPositionPixel][YPositionPixel -i]) == 0:
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
    def NotIn(self, Point):
        for Circle in self.CirclesInfo:
            thx = (Circle[1][0]-Circle[0][0])*0.25
            thy = (Circle[2][1]-Circle[3][1])*0.25
            if ((Circle[0][0] - thx  < Point[0])&(Circle[1][0] + thx > Point[0])&(Circle[3][1] - thy < Point[1])&(Circle[2][1] + thy > Point[1])):
                return False
        return True

    def CheckCenter(self, center, Info):
        for i in range(len(self.Centers)):
            XDifference = abs(self.Centers[i][0] - center[0])
            YDifference = abs(self.Centers[i][1] - center[1])
            if (((XDifference+YDifference)/2) < 10):
                self.Centers[i] = self.GetMiddlePoint(self.Centers[i], center)
                if self.CirclesInfo[i][0][0] > Info[0][0]:
                    self.CirclesInfo[i][0] = Info[0]
                if self.CirclesInfo[i][1][0] < Info[1][0]:
                    self.CirclesInfo[i][1] = Info[1]
                if self.CirclesInfo[i][2][1] < Info[2][1]:
                    self.CirclesInfo[i][2] = Info[2]
                if self.CirclesInfo[i][3][1] > Info[3][1]:
                    self.CirclesInfo[i][3] = Info[3]
                return 0
        self.Centers.append(center)
        self.CirclesInfo.append(Info)
