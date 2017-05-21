#!/usr/bin/python
# -*- coding: utf-8 -*-

# Library imports
import numpy as np


class Enviroment3d(object):

    def __init__(self,s12,s13,s14,s23,s24,s34):
        self.CameraCenterPrint = [75,75,600]
        self.CameraCenter = np.array([[75],[75],[600]])
        self.HeightPixels = 960
        self.WidthPixels = 1280
        self.Pixel2mmX = ( 1944 * 1.4*10**(-3))/self.HeightPixels
        self.Pixel2mmY = ( 2592 * 1.4*10**(-3))/self.WidthPixels        
        self.RotationMatrix = []
        self.Focal = 3.60
        self.s12 = s12
        self.s13 = s13
        self.s14 = s14
        self.s23 = s23
        self.s24 = s24
        self.s34 = s34
        self.points = []
        self.d1
        self.d2
        self.d3
        self.d4

    #Functions to test the algorith with theoretical points
    def GetRotationMatrix(self,x,y,z):
        d2r=np.pi/180
        thx=x*d2r
        thy=y*d2r 
        thz=z*d2r
        Rx=np.array([[1, 0, 0],
             [0, np.cos(thx), -np.sin(thx)],
             [0, np.sin(thx),  np.cos(thx)]]) 
        Ry=np.array([[np.cos(thy), 0, np.sin(thy)],
             [0, 1, 0],
             [-np.sin(thy), 0, np.cos(thy)]])
        Rz=np.array([[np.cos(thz), -np.sin(thz), 0],
             [np.sin(thz),  np.cos(thz), 0],
             [0, 0, 1]])
        R = Rz.dot(Ry.dot(Rx))
        self.RotationMatrix = np.linalg.inv(R)

    def AddPointsPicture(self,x,y):
        self.points.append([x,y])

    def World2Camera(self,Pi):
        v = np.array([[Pi[0]],[Pi[1]],[Pi[2]]])
        Vc = (self.RotationMatrix).dot(v-self.CameraCenter)
        return Vc

    def Camera2Picture(self, Pic):
        Vc = np.array([[Pic[0]],[Pic[1]],[Pic[2]]])
        Qc = Vc*(self.Focal/(Vc[2]))
        Qc = Qc*(-1)
        return Qc


    #Functions to test the algorithm with real data
    def Pixel2Camera(self, Points):
        result = []
        for point in Points:
             result.append([((self.HeightPixels/2) - point[0])*self.Pixel2mmX,(point[1]- (self.WidthPixels/2))*self.Pixel2mmY])
        print result
        return result
    
    def AddPointsTest(self,result):
        for point in result:
            self.AddPointsPicture(point[0],point[1])

    # Find distances
    def d1(self):
        self.d1 = np.sqrt((self.s12)**2.0 * (self.Fi(1))**2.0 / (self.H12_2() + (self.Focal**2.0)*(1 - self.C12())**2.0))
        #d12 = np.sqrt((self.s13)**2.0 * (self.Fi(1))**2.0 / (self.H13_2() + (self.Focal**2.0)*(1 - self.C13())**2.0))
        return self.d1
    def d2(self):
        self.d2 = self.C12()*self.Fi(2)*self.d1/self.Fi(1)
        return self.d2
    def d3(self):
        self.d3 = self.C13()*self.Fi(3)*self.d1/self.Fi(1)
        return self.d3
    def d4(self):
        self.d4 = self.C14()*self.Fi(4)*self.d1/self.Fi(1)
        return self.d4
        
    def FindF(self):
        return np.sqrt((self.s13**2.0 * self.H12_2() - self.s12**2.0 * self.H13_2()) / (self.s12**2.0 * (1 - self.C13())**2.0 - self.s13**2.0 * (1 - self.C12())**2.0))

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

    ## Bi: Twice the area of the tirangles formed by the image points
    def B1(self):
        #B1 = x1(y3 - y2) + y1 (x2 - x3) + y2*x3 - x2*y3
        return self.x1()*(self.y3()-self.y2()) + self.y1()*(self.x2()-self.x3()) + self.y2()*self.x3() - self.x2()*self.y3()
    def B2(self):
        #B2 = x1(y4 - y2) + y1 (x2 - x4) + y2*x4 - x2*y4
        return self.x1()*(self.y4()-self.y2()) + self.y1()*(self.x2()-self.x4()) + self.y2()*self.x4() - self.x2()*self.y4()
    def B3(self):
        #B3 = x1(y4 - y3) + y1 (x3 - x4) + y3*x4 - x3*y4
        return (self.x1()*(self.y4()-self.y3()) + self.y1()*(self.x3()-self.x4()) + self.y3()*self.x4() - self.x3()*self.y4())
    def B4(self):
        #B4 = x2(y4 - y3) + y2 (x3 - x4) + y3*x4 - x3*y4
        return (self.x2()*(self.y4()-self.y3()) + self.y2()*(self.x3()-self.x4()) + self.y3()*self.x4() - self.x3()*self.y4())
    
    ## Ai: Area of the four differents triangles 
    def A1(self):
        #Area Triangle P1P2P3
        return ((self.s12**2.0 + self.s13**2.0 + self.s23**2.0)**2.0 -2*(self.s12**4.0 + self.s13**4.0 + self.s23**4.0))**(0.5)/4.0
    def A2(self):
        #Area Triangle P1P2P4
        return ((self.s12**2.0 + self.s14**2.0 + self.s24**2.0)**2.0 -2*(self.s12**4.0 + self.s14**4.0 + self.s24**4.0))**(0.5)/4.0
    def A3(self):
        #Area Triangle P1P3P4
        return ((self.s13**2.0 + self.s14**2.0 + self.s34**2.0)**2.0 -2*(self.s13**4.0 + self.s14**4.0 + self.s34**4.0))**(0.5)/4.0
    def A4(self):
        #Area Triangle P2P3P4
        return ((self.s23**2.0 + self.s24**2.0 + self.s34**2.0)**2.0 -2*(self.s23**4.0 + self.s24**4.0 + self.s34**4.0))**(0.5)/4.0

    ## Cij: Untiless variable used to calculate relationship between the center of projection and the target
    def C12(self):
        return (self.B3()*self.A4())/(self.A3()*self.B4())
    def C13(self):
        return (self.B2()*self.A4())/(self.A2()*self.B4())
    def C14(self):
        return (self.B1()*self.A4())/(self.A1()*self.B4())
    def C23(self):
        return (self.B2()*self.A3())/(self.A2()*self.B3())
    def C24(self):
        return (self.B1()*self.A3())/(self.A1()*self.B3())
    def C34(self):
        return (self.B1()*self.A2())/(self.A1()*self.B2())

    ## Hij: Unit variable used to calculate the effective focal length

    def H12_2(self):
        return (self.x1() - self.C12()*self.x2())**2.0 + (self.y1() - self.C12()*self.y2())**2.0 
    def H13_2(self):
        return (self.x1() - self.C13()*self.x3())**2.0 + (self.y1() - self.C13()*self.y3())**2.0        
    def H14_2(self):
        return (self.x1() - self.C14()*self.x4())**2.0 + (self.y1() - self.C14()*self.y4())**2.0        
    def H23_2(self):
        return (self.x2() - self.C23()*self.x3())**2.0 + (self.y2() - self.C23()*self.y3())**2.0
    def H24_2(self):
        return (self.x2() - self.C24()*self.x4())**2.0 + (self.y2() - self.C24()*self.y4())**2.0
    def H34_2(self):
        return (self.x3() - self.C34()*self.x4())**2.0 + (self.y3() - self.C34()*self.y4())**2.0



    ## Fi: Magnitude of the vector Qi 
    def Fi(self, point):
        if (point == 1):
            return np.sqrt(self.x1()**2.0 + self.y1()**2.0 + self.Focal**2.0)
        elif (point == 2):
            return np.sqrt(self.x2()**2.0 + self.y2()**2.0 + self.Focal**2.0)
        elif (point == 3):
            return np.sqrt(self.x3()**2.0 + self.y3()**2.0 + self.Focal**2.0)
        elif (point == 4):
            return np.sqrt(self.x4()**2.0 + self.y4()**2.0 + self.Focal**2.0)
        


   
