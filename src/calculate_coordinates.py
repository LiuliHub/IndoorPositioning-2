#!/usr/bin/python
# -*- coding: utf-8 -*-

# Library imports
import numpy as np
from transformations import *

class Enviroment3d(object):

    def __init__(self,s12,s13,s14,s23,s24,s34):
        self.CameraCenterPrint = [75,75,600]
        self.CameraCenter = np.array([[75],[75],[600]])
        self.HeightPixels = 384
        self.WidthPixels = 512
        self.Pixel2mmX = ( 1944 * 1.4*10**(-3))/self.HeightPixels
        self.Pixel2mmY = ( 2592 * 1.4*10**(-3))/self.WidthPixels        
        self.RotationMatrix = []
        self.Focal = 3.6
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
        #self.T

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
        return result
    
    def AddPointsTest(self,result):
        for point in result:
            self.AddPointsPicture(point[0],point[1])

    # Find distances
    def d1(self):
        factor1 = self.s12*(1/self.R12())*self.Fi(1)       
        factor2 = self.s13*(1/self.R13())*self.Fi(1)
        factor3 = self.s14*(1/self.R14())*self.Fi(1)
        factor4 = self.s23/(self.R23()*self.C12())*self.Fi(1)
        factor5 = self.s24/(self.R24()*self.C12())*self.Fi(1)
        factor6 = self.s34/(self.R34()*self.C13())*self.Fi(1)
        factor = [factor1,factor2,factor3,factor4,factor5,factor6]
        for i in range(0,2): 
            factor.remove(np.max(factor))               
            factor.remove(np.min(factor))               
              
        self.d1 = np.average(factor)
        #self.d1 = np.sqrt((self.s12)**2.0 * (self.Fi(1))**2.0 / (self.H12_2() + (self.Focal**2.0)*(1 - self.C12())**2.0))
        #d12 = np.sqrt((self.s13)**2.0 * (self.Fi(1))**2.0 / (self.H13_2() + (self.Focal**2.0)*(1 - self.C13())**2.0))
        return self.d1
    def d2(self):
        self.d2 = self.C12()*self.Fi(2)*self.d1/self.Fi(1)
        return self.d2
    def d3(self):
        factor1 = self.C13()*self.Fi(3)*self.d1/self.Fi(1)
        factor2 = self.C23()*self.Fi(3)*self.d2/self.Fi(2)
        self.d3 = np.average([factor1, factor2])
        return self.d3
    def d4(self):
        factor1 = self.C14()*self.Fi(4)*self.d1/self.Fi(1)
        factor2 = self.C24()*self.Fi(4)*self.d2/self.Fi(2)
        factor3 = self.C34()*self.Fi(4)*self.d3/self.Fi(3)
        
        self.d4 = np.average([factor1, factor2, factor3])
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

    def R12(self):
        return(np.sqrt(self.H12_2() + (self.Focal**2)*((1-self.C12())**2)))
    def R13(self):
        return(np.sqrt(self.H13_2() + (self.Focal**2)*((1-self.C13())**2)))
    def R14(self):
        return(np.sqrt(self.H14_2() + (self.Focal**2)*((1-self.C14())**2)))
    def R23(self):
        return(np.sqrt(self.H23_2() + (self.Focal**2)*((1-self.C23())**2)))
    def R24(self):
        return(np.sqrt(self.H24_2() + (self.Focal**2)*((1-self.C24())**2)))
    def R34(self):
        return(np.sqrt(self.H34_2() + (self.Focal**2)*((1-self.C34())**2)))

    '''    
    def P1C(self):
        factor = self.s12*(1/self.R12())
        return factor*np.array([-self.x1(),-self.y1(), self.Focal]) + np.array([0,0,self.Focal]) 
    def P2C(self):
        factor = self.C12()*self.s12*(1/self.R12())
        return factor*np.array([-self.x2(),-self.y2(), self.Focal]) + np.array([0,0,self.Focal]) 
    def P3C(self):
        factor = self.C13()*self.s12*(1/self.R12())
        return factor*np.array([-self.x3(),-self.y3(), self.Focal]) + np.array([0,0,self.Focal]) 
    def P4C(self):
        factor = self.C14()*self.s12*(1/self.R12())
        return factor*np.array([-self.x4(),-self.y4(), self.Focal]) + np.array([0,0,self.Focal]) 
    '''
    def PrintP1C(self):
        factor = self.s12*(1/self.R12())        
        p1 = factor*np.array([self.x1(),self.y1(), self.Focal])         
        factor2 = self.s13*(1/self.R13())
        p2 = factor2*np.array([self.x1(),self.y1(), self.Focal])         
        factor3 = self.s14*(1/self.R14())
        p3 = factor3*np.array([self.x1(),self.y1(), self.Focal])         
        factor4 = self.s23/(self.R23()*self.C12())
        p4 = factor4*np.array([self.x1(),self.y1(), self.Focal])         
        factor5 = self.s24/(self.R24()*self.C12())
        p5 =  factor5*np.array([self.x1(),self.y1(), self.Focal])         
        factor6 = self.s34/(self.R34()*self.C13())        
        p6 = factor6*np.array([self.x1(),self.y1(), self.Focal])                 
        X = [p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]]                 
        Y = [p1[1], p2[1], p3[1], p4[1], p5[1], p6[1]]                 
        Z = [p1[2], p2[2], p3[2], p4[2], p5[2], p6[2]]
        for i in range(0,2): 
            X.remove(np.max(X))               
            Y.remove(np.max(Y))               
            Z.remove(np.max(Z))
            X.remove(np.min(X))               
            Y.remove(np.min(Y))               
            Z.remove(np.min(Z))                
        print "P1C: "
        print p1
        print p2
        print p3
        print p4
        print p5
        print p6
        #print "Mediana: " str([np.mean(X), np.mean(Y),np.mean(Z)])
        print "Mitjana: "+ str([np.average(X), np.average(Y),np.average(Z)])
    def PrintP2C(self):
        factor = self.C12()*self.s12*(1/self.R12())        
        p1 = factor*np.array([self.x2(),self.y2(), self.Focal])         
        factor2 = self.C12()*self.s13*(1/self.R13())
        p2 = factor2*np.array([self.x2(),self.y2(), self.Focal])         
        factor3 = self.C12()*self.s14*(1/self.R14())
        p3 = factor3*np.array([self.x2(),self.y2(), self.Focal])         
        factor4 = self.C12()*self.s23/(self.R23()*self.C12())
        p4 = factor4*np.array([self.x2(),self.y2(), self.Focal])         
        factor5 = self.C12()*self.s24/(self.R24()*self.C12())
        p5 =  factor5*np.array([self.x2(),self.y2(), self.Focal])         
        factor6 = self.C12()*self.s34/(self.R34()*self.C13())        
        p6 = factor6*np.array([self.x2(),self.y2(), self.Focal])                 
        X = [p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]]                 
        Y = [p1[1], p2[1], p3[1], p4[1], p5[1], p6[1]]                 
        Z = [p1[2], p2[2], p3[2], p4[2], p5[2], p6[2]] 
        for i in range(0,2): 
            X.remove(np.max(X))               
            Y.remove(np.max(Y))               
            Z.remove(np.max(Z))
            X.remove(np.min(X))               
            Y.remove(np.min(Y))               
            Z.remove(np.min(Z))              
        print "P2C: "
        print p1
        print p2
        print p3
        print p4
        print p5
        print p6
        #print "Mediana: " str([np.mean(X), np.mean(Y),np.mean(Z)])
        print "Mitjana: "+ str([np.average(X), np.average(Y),np.average(Z)])
    def PrintP3C(self):
        factor = self.C13()*self.s12*(1/self.R12())        
        p1 = factor*np.array([self.x3(),self.y3(), self.Focal])         
        factor2 = self.C13()*self.s13*(1/self.R13())
        p2 = factor2*np.array([self.x3(),self.y3(), self.Focal])         
        factor3 = self.C13()*self.s14*(1/self.R14())
        p3 = factor3*np.array([self.x3(),self.y3(), self.Focal])         
        factor4 = self.C13()*self.s23/(self.R23()*self.C12())
        p4 = factor4*np.array([self.x3(),self.y3(), self.Focal])         
        factor5 = self.C13()*self.s24/(self.R24()*self.C12())
        p5 =  factor5*np.array([self.x3(),self.y3(), self.Focal])         
        factor6 = self.C13()*self.s34/(self.R34()*self.C13())        
        p6 = factor6*np.array([self.x3(),self.y3(), self.Focal])                 
        X = [p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]]                 
        Y = [p1[1], p2[1], p3[1], p4[1], p5[1], p6[1]]                 
        Z = [p1[2], p2[2], p3[2], p4[2], p5[2], p6[2]]
        for i in range(0,2): 
            X.remove(np.max(X))               
            Y.remove(np.max(Y))               
            Z.remove(np.max(Z))
            X.remove(np.min(X))               
            Y.remove(np.min(Y))               
            Z.remove(np.min(Z))
        print "P3C: "
        print p1
        print p2
        print p3
        print p4
        print p5
        print p6
        #print "Mediana: " str([np.mean(X), np.mean(Y),np.mean(Z)])
        print "Mitjana: "+ str([np.average(X), np.average(Y),np.average(Z)])
        
    def PrintP4C(self):
        factor = self.C14()*self.s12*(1/self.R12())        
        p1 = factor*np.array([self.x4(),self.y4(), self.Focal])         
        factor2 = self.C14()*self.s13*(1/self.R13())
        p2 = factor2*np.array([self.x4(),self.y4(), self.Focal])         
        factor3 = self.C14()*self.s14*(1/self.R14())
        p3 = factor3*np.array([self.x4(),self.y4(), self.Focal])         
        factor4 = self.C14()*self.s23/(self.R23()*self.C12())
        p4 = factor4*np.array([self.x4(),self.y4(), self.Focal])         
        factor5 = self.C14()*self.s24/(self.R24()*self.C12())
        p5 =  factor5*np.array([self.x4(),self.y4(), self.Focal])         
        factor6 = self.C14()*self.s34/(self.R34()*self.C13())        
        p6 = factor6*np.array([self.x4(),self.y4(), self.Focal])                 
        X = [p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]]                 
        Y = [p1[1], p2[1], p3[1], p4[1], p5[1], p6[1]]                 
        Z = [p1[2], p2[2], p3[2], p4[2], p5[2], p6[2]]
        for i in range(0,2): 
            X.remove(np.max(X))               
            Y.remove(np.max(Y))               
            Z.remove(np.max(Z))
            X.remove(np.min(X))               
            Y.remove(np.min(Y))               
            Z.remove(np.min(Z))              
        print "P4C: "
        print p1
        print p2
        print p3
        print p4
        print p5
        print p6
        #print "Mediana: " str([np.mean(X), np.mean(Y),np.mean(Z)])
        print "Mitjana: "+ str([np.average(X), np.average(Y),np.average(Z)])
                
    def P1C(self):
        factor = self.s12*(1/self.R12())        
        p1 = factor*np.array([self.x1(),self.y1(), self.Focal])         
        factor2 = self.s13*(1/self.R13())
        p2 = factor2*np.array([self.x1(),self.y1(), self.Focal])         
        factor3 = self.s14*(1/self.R14())
        p3 = factor3*np.array([self.x1(),self.y1(), self.Focal])         
        factor4 = self.s23/(self.R23()*self.C12())
        p4 = factor4*np.array([self.x1(),self.y1(), self.Focal])         
        factor5 = self.s24/(self.R24()*self.C12())
        p5 =  factor5*np.array([self.x1(),self.y1(), self.Focal])         
        factor6 = self.s34/(self.R34()*self.C13())        
        p6 = factor6*np.array([self.x1(),self.y1(), self.Focal])                 
        X = [p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]]                 
        Y = [p1[1], p2[1], p3[1], p4[1], p5[1], p6[1]]                 
        Z = [p1[2], p2[2], p3[2], p4[2], p5[2], p6[2]]
        for i in range(0,2): 
            X.remove(np.max(X))               
            Y.remove(np.max(Y))               
            Z.remove(np.max(Z))
            X.remove(np.min(X))               
            Y.remove(np.min(Y))               
            Z.remove(np.min(Z))
        #return [np.average([np.max(X),np.min(X)]), np.average([np.max(Y),np.min(Y)]),np.average([np.max(Z),np.min(Z)])]
        return [np.average(X), np.average(Y),np.average(Z)]
    def P2C(self):
        factor = self.C12()*self.s12*(1/self.R12())        
        p1 = factor*np.array([self.x2(),self.y2(), self.Focal])         
        factor2 = self.C12()*self.s13*(1/self.R13())
        p2 = factor2*np.array([self.x2(),self.y2(), self.Focal])         
        factor3 = self.C12()*self.s14*(1/self.R14())
        p3 = factor3*np.array([self.x2(),self.y2(), self.Focal])         
        factor4 = self.C12()*self.s23/(self.R23()*self.C12())
        p4 = factor4*np.array([self.x2(),self.y2(), self.Focal])         
        factor5 = self.C12()*self.s24/(self.R24()*self.C12())
        p5 =  factor5*np.array([self.x2(),self.y2(), self.Focal])         
        factor6 = self.C12()*self.s34/(self.R34()*self.C13())        
        p6 = factor6*np.array([self.x2(),self.y2(), self.Focal])                 
        X = [p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]]                 
        Y = [p1[1], p2[1], p3[1], p4[1], p5[1], p6[1]]                 
        Z = [p1[2], p2[2], p3[2], p4[2], p5[2], p6[2]]  
        for i in range(0,2): 
            X.remove(np.max(X))               
            Y.remove(np.max(Y))               
            Z.remove(np.max(Z))
            X.remove(np.min(X))               
            Y.remove(np.min(Y))               
            Z.remove(np.min(Z))     
        #return [np.average([np.max(X),np.min(X)]), np.average([np.max(Y),np.min(Y)]),np.average([np.max(Z),np.min(Z)])]        
        return [np.average(X), np.average(Y),np.average(Z)]
    def P3C(self):
        factor = self.C13()*self.s12*(1/self.R12())        
        p1 = factor*np.array([self.x3(),self.y3(), self.Focal])         
        factor2 = self.C13()*self.s13*(1/self.R13())
        p2 = factor2*np.array([self.x3(),self.y3(), self.Focal])         
        factor3 = self.C13()*self.s14*(1/self.R14())
        p3 = factor3*np.array([self.x3(),self.y3(), self.Focal])         
        factor4 = self.C13()*self.s23/(self.R23()*self.C12())
        p4 = factor4*np.array([self.x3(),self.y3(), self.Focal])         
        factor5 = self.C13()*self.s24/(self.R24()*self.C12())
        p5 =  factor5*np.array([self.x3(),self.y3(), self.Focal])         
        factor6 = self.C13()*self.s34/(self.R34()*self.C13())        
        p6 = factor6*np.array([self.x3(),self.y3(), self.Focal])                 
        X = [p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]]                 
        Y = [p1[1], p2[1], p3[1], p4[1], p5[1], p6[1]]                 
        Z = [p1[2], p2[2], p3[2], p4[2], p5[2], p6[2]]
        for i in range(0,2): 
            X.remove(np.max(X))               
            Y.remove(np.max(Y))               
            Z.remove(np.max(Z))
            X.remove(np.min(X))               
            Y.remove(np.min(Y))               
            Z.remove(np.min(Z))
        #return [np.average([np.max(X),np.min(X)]), np.average([np.max(Y),np.min(Y)]),np.average([np.max(Z),np.min(Z)])]
        return [np.average(X), np.average(Y),np.average(Z)]         
    def P4C(self):
        factor = self.C14()*self.s12*(1/self.R12())        
        p1 = factor*np.array([self.x4(),self.y4(), self.Focal])         
        factor2 = self.C14()*self.s13*(1/self.R13())
        p2 = factor2*np.array([self.x4(),self.y4(), self.Focal])         
        factor3 = self.C14()*self.s14*(1/self.R14())
        p3 = factor3*np.array([self.x4(),self.y4(), self.Focal])         
        factor4 = self.C14()*self.s23/(self.R23()*self.C12())
        p4 = factor4*np.array([self.x4(),self.y4(), self.Focal])         
        factor5 = self.C14()*self.s24/(self.R24()*self.C12())
        p5 =  factor5*np.array([self.x4(),self.y4(), self.Focal])         
        factor6 = self.C14()*self.s34/(self.R34()*self.C13())        
        p6 = factor6*np.array([self.x4(),self.y4(), self.Focal])                 
        X = [p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]]                 
        Y = [p1[1], p2[1], p3[1], p4[1], p5[1], p6[1]]                 
        Z = [p1[2], p2[2], p3[2], p4[2], p5[2], p6[2]] 
        for i in range(0,2): 
            X.remove(np.max(X))               
            Y.remove(np.max(Y))               
            Z.remove(np.max(Z))
            X.remove(np.min(X))               
            Y.remove(np.min(Y))               
            Z.remove(np.min(Z))
        #return [np.average([np.max(X),np.min(X)]), np.average([np.max(Y),np.min(Y)]),np.average([np.max(Z),np.min(Z)])]
        return [np.average(X), np.average(Y),np.average(Z)]             
    def Tmatrix(self,P1,P2,P3,P4):
        T11 = (P4[1]*(self.P3C()[0]-self.P1C()[0])-P3[1]*(self.P4C()[0]-self.P1C()[0]) )/( P3[0]*P4[1]-P4[0]*P3[1])
        T21 = (P4[1]*(self.P3C()[1]-self.P1C()[1])-P3[1]*(self.P4C()[1]-self.P1C()[1]) )/( P3[0]*P4[1]-P4[0]*P3[1])
        T31 = (P4[1]*(self.P3C()[2]-self.P1C()[2])-P3[1]*(self.P4C()[2]-self.P1C()[2]) )/( P3[0]*P4[1]-P4[0]*P3[1])
        T12 = (P3[0]*(self.P4C()[0]-self.P1C()[0])-P4[0]*(self.P3C()[0]-self.P1C()[0]) )/( P3[0]*P4[1]-P4[0]*P3[1])
        T22 = (P3[0]*(self.P4C()[1]-self.P1C()[1])-P4[0]*(self.P3C()[1]-self.P1C()[1]) )/( P3[0]*P4[1]-P4[0]*P3[1])
        T32 = (P3[0]*(self.P4C()[2]-self.P1C()[2])-P4[0]*(self.P3C()[2]-self.P1C()[2]) )/( P3[0]*P4[1]-P4[0]*P3[1])
        T14 = self.P1C()[0]
        T24 = self.P1C()[1]
        T34 = self.P1C()[2]
        T13 = T21*T32 - T22*T31
        T23 = T12*T31 - T11*T32
        T33 = T11*T22 - T12*T21
        self.T = np.array([[T11,T12,T13,T14],[T21,T22,T23,T24],[T31,T32,T33,T34],[0,0,0,1]])
    def GetPositonXYZ(self):
        
        scale, shear, angles, trans, persp = decompose_matrix(self.T)
        TT = self.T.T
        o = np.array([[0],[0],[0],[1]])
        transO = np.matmul(o.T,np.linalg.inv(TT))
        self.d1()
        self.d2()
        self.d3()
        self.d4()

        return[transO[0][0],transO[0][1],transO[0][2],angles[0],angles[1],angles[2]]
        #return[trans[0],trans[1],trans[2],angles[0],angles[1],angles[2],transO]
        '''
        self.d1()
        self.d2()
        self.d3()
        self.d4()
        X0 = -self.T[0][0]*self.T[0][3] - self.T[1][0]*self.T[1][3] - self.T[2][0]*self.T[2][3]
        Y0 = -self.T[0][1]*self.T[0][3] - self.T[1][1]*self.T[1][3] - self.T[2][1]*self.T[2][3]
        Z0 = -self.T[0][2]*self.T[0][3] - self.T[1][2]*self.T[1][3] - self.T[2][2]*self.T[2][3]
        if (self.T[2][2] != 1):
            b0 = np.arccos(self.T[2][2])
            a0 = np.arctan(-self.T[1][2]/self.T[0][2])
            c0 = np.arctan(self.T[2][1]/self.T[2][0])
            if(self.T[0][2]>0): 
                a0= a0 + np.pi
            if(self.T[2][0]<0):
                b0 = b0 + np.pi
        else:
            b0 = 0
            c0 = 0
            a0 = np.arctan(self.T[0][1]/self.T[1][1])
            if(self.T[1][1]>0):
                 a0= a0 + np.pi
        a0 = np.rad2deg(a0)
        b0 = np.rad2deg(b0)
        c0 = np.rad2deg(c0)
        while a0 > 360:
            a0 = a0 - 360
        while b0 > 360:
            b0 = b0 - 360
        while c0 > 360:
            b0 = b0 - 360
        return [X0,Y0,Z0,a0,b0,c0]
        '''
    def IsAGoodMesurement(self):
        factor1 = round(self.s12*(1/self.R12())*self.Fi(1))     
        factor2 = round(self.s13*(1/self.R13())*self.Fi(1))
        factor3 = round(self.s14*(1/self.R14())*self.Fi(1))
        factor4 = round(self.s23/(self.R23()*self.C12())*self.Fi(1))
        factor5 = round(self.s24/(self.R24()*self.C12())*self.Fi(1))
        factor6 = round(self.s34/(self.R34()*self.C13())*self.Fi(1))
        print [factor1,factor2,factor3, factor4, factor5, factor6]       
        return (factor1 == factor2 == factor3 == factor4 == factor5 == factor6)
    
    def AblePrintDistance(self):
        return ((self.d1<900)and(self.d2<900)and(self.d2<900)and(self.d2<900))