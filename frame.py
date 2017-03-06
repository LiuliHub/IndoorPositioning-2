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
        fn = "./%i.jpg" % int(time.time())
        image.save(fn)

    def DrawInImage(self,ArrayPixels):
        matrix = self.PixelMap
        for pixel in ArrayPixels:
            self.PixelMap[pixel[0]][pixel[1]] = (0,255,0)

        return 0
    def GetPuzzleCircles(self):
        return 0