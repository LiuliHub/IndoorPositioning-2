#!/usr/bin/python
# -*- coding: utf-8 -*-

# Library imports
from img import *
from PIL import Image
import time


class Frame(object):
    def __init__(self):
        self.PixelMap = []

    def ReadFrame(self, FileName):
        image = Image.open(FileName)
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
        if((Pixel[0]>100)&(Pixel[1]>100)&(Pixel[2]>100)):
            #print "White"
            return 0
        elif((Pixel[0]<60)&(Pixel[1]<60)&(Pixel[2]<60)):
            #print "Black"
            return 1
        else:
            #print "Other"
            return 2

    def GetPuzzleCircles(self):
        State = 0
        BlackPuzzle = []
        BlackPiece = []
        for x in range(len(self.PixelMap)):
            for y in range(len(self.PixelMap[x])):
                Pixel = self.PixelMap[x][y]
                colour = self.WitchColorPixel(Pixel)
                if State == 0:
                    if (colour == 0):       #White
                        State = 1
                    elif(colour == 1):      #Black
                        State = 0
                    else:                   #Other
                        State = 1
                elif State == 1:
                    if (colour == 0):       #White
                        State = 1
                    elif(colour == 1):      #Black
                        State = 2
                    else:                   #Other
                        State = 1
                else:
                    if (colour == 0):      #White
                        State = 1
                        BlackPuzzle.append(BlackPiece)
                        BlackPiece = []
                    elif(colour == 1):      #Black
                        State = 2
                        BlackPiece.append([x,y])
                    else:                   #Other
                        State = 0
                        BlackPuzzle.append(BlackPiece)
                        BlackPiece = []

            

        return BlackPuzzle