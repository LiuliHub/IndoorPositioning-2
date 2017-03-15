#!/usr/bin/python
# -*- coding: utf-8 -*-

# Library imports
from img import *
from PIL import Image, ImageFilter
import time


class Frame(object):
    def __init__(self):
        self.PixelMap = []
        self.Edge =[]


    def GetFrameInfo(self):
        return [len(self.PixelMap),len(self.PixelMap[0])]
    def ReadFrame(self, FileName, thresh):
        image = Image.open(FileName)
        image = image.point(lambda i: 255 if i > thresh else 0)
        pix = image.load()
        X, Y = image.size[0], image.size[1]
        data = [[pix[x,y] for x in range(X)] for y in range(Y)] 
        self.PixelMap = data  

    def save(self):
        i = img(self.PixelMap,'RGB')
        image = Image.new(format(i),(get_w(i),get_h(i)))
        image.putdata([pixel for F in matrix(i) for pixel in F])
        fn = "./Img_test/%i.jpg" % int(time.time())
        image.save(fn)

    def DrawInImage(self,ArrayPixels,thickness):
        matrix = self.PixelMap
        for pixel in ArrayPixels:
            if(thickness == 1):
                self.PixelMap[pixel[0]][pixel[1]] = (0,255,0)
            else:
                for i in range(0, thickness):
                    self.PixelMap[pixel[0]+i][pixel[1]] = (0,255,0) 

        return 0

    def WitchColorPixel(self, Pixel):
        if((Pixel[0]<60)&(Pixel[1]<60)&(Pixel[2]<60)):
           #print "Black"
            return 1
        else:
             #print "White"
            return 0
                              

    def GetPuzzleCircles(self):
        State = 1
        BlackPuzzle = []
        for x in range(len(self.PixelMap)):
            for y in range(len(self.PixelMap[x])):
                Pixel = self.PixelMap[x][y]
                colour = self.WitchColorPixel(Pixel)
                if State == 1:
                    if (colour == 0):       #White
                        State = 1
                    else:                   #Black
                        State = 2
                else:
                    if (colour == 0):      #White
                        State = 1
                    else:      #Black
                        State = 2
                        BlackPuzzle.append([x,y])
        return BlackPuzzle

    def saveEdge(self):
        i = img(self.Edge,'RGB')
        image = Image.new(format(i),(get_w(i),get_h(i)))
        image.putdata([pixel for F in matrix(i) for pixel in F])
        fn = "./Img_test/%i.jpg" % int(time.time())
        image.save(fn)
    def DrawInImageEdge(self,ArrayPixels,thickness):
        for pixel in ArrayPixels:
            if(thickness == 1):
                self.Edge[pixel[0]][pixel[1]] = (0,255,0)
            else:
                for i in range(0, thickness):
                    self.Edge[pixel[0]+i][pixel[1]] = (0,255,0) 

        return 0
    def GetWhiteEdges(self):
        White = []
        i = 0
        for x in range(len(self.Edge)):
            for y in range(len(self.Edge[x])):
                Pixel = self.Edge[x][y]
                if((Pixel[0]>240)&(Pixel[1]>240)&(Pixel[2]>240)):
                    i= i+1
                    White.append(Pixel)
        print str(i)
        return White
    def FindEdges(self, FileName):
        image = Image.open(FileName)
        image = image.filter(ImageFilter.FIND_EDGES)
        thresh = 100 # Change at your discretion
        image = image.point(lambda i: 255 if i > thresh else 0)
        pix = image.load()
        X, Y = image.size[0], image.size[1]
        data = [[pix[x,y] for x in range(X)] for y in range(Y)] 
        self.Edge= data  