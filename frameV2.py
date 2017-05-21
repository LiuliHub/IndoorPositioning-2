#!/usr/bin/python
# -*- coding: utf-8 -*-

# Library imports
from img import *
from PIL import Image, ImageFilter
import time
from numpy import *


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
    def CheckLine(self,p1,p2,p3):

        return abs((self.Centers[p1-1][0]*(self.Centers[p2-1][1]-self.Centers[p3-1][1]) + self.Centers[p2-1][0]*(self.Centers[p3-1][1]-self.Centers[p1-1][1]) + self.Centers[p3-1][0]*(self.Centers[p1-1][1]-self.Centers[p2-1][1]))/2)

    def perp(self, a ) :
        b = empty_like(a)
        b[0] = -a[1]
        b[1] = a[0]
        return b

        # line segment a given by endpoints a1, a2
        # line segment b given by endpoints b1, b2
        # return 
    def seg_intersect(self, a1,a2, b1,b2) :
        da = array(a2) - array(a1) 
        db = array(b2) - array(b1) 
        dp = array(a1) - array(b1)
        dap = self.perp(da)
        denom = dot( dap, db)
        num = dot( dap, dp )
        return (num / denom.astype(float))*db + b1

    def GetLinedPoints(self):
        i=0
        AreaMin = 0
        Combination = [] 
        while(i<10):
            if(i==0):
                AreaMin = self.CheckLine(1,2,3)
                Combination = [1,2,3]
            elif(i==1):
                a = self.CheckLine(1,2,4)
                if(a  < AreaMin):
                    AreaMin = a
                    Combination = [1,2,4]
            elif(i==2):
                a = self.CheckLine(1,2,5)
                if(a  < AreaMin):
                    AreaMin = a
                    Combination = [1,2,5]
            elif(i==3):
                a = self.CheckLine(1,3,4)
                if(a  < AreaMin):
                    AreaMin = a
                    Combination = [1,3,4]
            elif(i==4):
                a = self.CheckLine(1,3,5)
                if(a  < AreaMin):
                    AreaMin = a
                    Combination = [1,3,5]
            elif(i==5):
                a = self.CheckLine(1,4,5)
                if(a  < AreaMin):
                    AreaMin = a
                    Combination = [1,4,5]
            elif(i==6):
                a = self.CheckLine(2,3,4)
                if(a  < AreaMin):
                    AreaMin = a
                    Combination = [2,3,4]
            elif(i==7):
                a = self.CheckLine(2,3,5)
                if(a  < AreaMin):
                    AreaMin = a
                    Combination = [2,3,5]
            elif(i==8):
                a = self.CheckLine(2,4,5)
                if(a  < AreaMin):
                    AreaMin = a
                    Combination = [2,4,5]
            else:
                a = self.CheckLine(3,4,5)
                if(a  < AreaMin):
                    AreaMin = a
                    Combination = [3,4,5]
            i=i+1
        return Combination
    def distance(self, Pi,Pj):
        return sqrt( abs(Pi[0]-Pj[0])**2.0 + abs(Pi[1]-Pj[1])**2.0 )   

    def GetOrderLinedPoints(self,linedpoints):
        if(abs(self.distance(self.Centers[linedpoints[0]-1],self.Centers[linedpoints[1]-1])) < abs(self.distance(self.Centers[linedpoints[2]-1],self.Centers[linedpoints[1]-1]))):
            return [linedpoints[2],linedpoints[0]]
        else:
             return [linedpoints[0],linedpoints[2]]
         

    def GetoOrderPoints(self,LinedPoints):
        PointsLeft = []
        for element in [1,2,3,4,5]:
            if element not in LinedPoints:
                PointsLeft.append(element)
        OrdenedLinedPoints = self.GetOrderLinedPoints(LinedPoints)
        intersection = self.seg_intersect(self.Centers[PointsLeft[0] - 1],self.Centers[OrdenedLinedPoints[0] - 1],self.Centers[PointsLeft[1] - 1],self.Centers[OrdenedLinedPoints[1] - 1])
        if (self.Centers[PointsLeft[0] - 1][0] < intersection[0] < self.Centers[OrdenedLinedPoints[0] - 1][0]):
            return [PointsLeft[0], PointsLeft[1], OrdenedLinedPoints[0],OrdenedLinedPoints[1]]
        else:
            return [PointsLeft[1], PointsLeft[0], OrdenedLinedPoints[0],OrdenedLinedPoints[1]]
            


