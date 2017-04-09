#!/usr/bin/python
# -*- coding: utf-8 -*-

# Library imports
import numpy as np

class Enviroment3d(object):

    def __init__(self,s12,s13,s14,s23,s24,s34):
        self.CameraCenter = np.array([[1],[1],[10]])
        self.RotationMatrix = np.array([[-1, 0, 0],[0, 1, 0],[0, 0, -1]])
        self.Focal = 0.36000
        self.s12 = s12
        self.s13 = s13
        self.s14 = s14
        self.s23 = s23
        self.s24 = s24
        self.s34 = s34
        self.points = []

    def AddPointsPicture(self,x,y):
        self.points.append([x,y])

    def World2Camera(self,x,y,z):
        v = np.array([[x],[y],[z]])
        Vc = (self.RotationMatrix).dot(v-self.CameraCenter)
        return Vc

    def Camera2Picture(self,x,y,z):
        Vc = np.array([[x],[y],[z]])
        Qc = Vc*1.0*self.Focal/(Vc[2])
        return Qc
    # Function return every x,y from every point 
    def x1(self):
        return self.points[0][0]
    def y1(self):
        return self.points[0][1]
    def x2(self):
        return self.points[1][0]
    def y2(self):
        return self.points[1][1]
    def x3(self):
        return self.points[2][0]
    def y3(self):
        return self.points[2][1]
    def x4(self):
        return self.points[3][0]
    def y4(self):
        return self.points[3][1]
    
    # Functions to make the algorithm

    def B1(self):
        #B1 = x1(y3 - y2) + y1 (x2 - x3) + y2*x3 - x2*y3
        return self.x1()*(self.y3()-self.y2()) + self.y1()*(self.x2()-self.x3()) + self.y2()*self.x3() - self.x2()*self.y3()
    def B2(self):
        #B2 = x1(y4 - y2) + y1 (x2 - x4) + y2*x4 - x2*y4
        return self.x1()*(self.y4()-self.y2()) + self.y1()*(self.x2()-self.x4()) + self.y2()*self.x4() - self.x2()*self.y4()
    def B3(self):
        #B3 = x1(y4 - y3) + y1 (x3 - x4) + y3*x4 - x3*y4
        return self.x1()*(self.y4()-self.y3()) + self.y1()*(self.x3()-self.x4()) + self.y3()*self.x4() - self.x3()*self.y4()
    def B4(self):
        #B4 = x2(y4 - y3) + y2 (x3 - x4) + y3*x4 - x3*y4
        return self.x2()*(self.y4()-self.y3()) + self.y2()*(self.x3()-self.x4()) + self.y3()*self.x4() - self.x3()*self.y4()
    def A1(self):
        #Area Triangle P1P2P3
        return ((self.s12**2 + self.s13**2 + self.s23**2)**2 -2*(self.s12**4 + self.s13**4 + self.s23**4))**(1/2)/4.0
    def A2(self):
        #Area Triangle P1P2P4
        return ((self.s12**2 + self.s14**2 + self.s24**2)**2 -2*(self.s12**4 + self.s14**4 + self.s24**4))**(1/2)/4.0
    def A3(self):
        #Area Triangle P1P3P4
        return ((self.s13**2 + self.s14**2 + self.s34**2)**2 -2*(self.s13**4 + self.s14**4 + self.s34**4))**(1/2)/4.0
    def A4(self):
        #Area Triangle P2P3P4
        return ((self.s23**2 + self.s24**2 + self.s34**2)**2 -2*(self.s23**4 + self.s24**4 + self.s34**4))**(1/2)/4.0