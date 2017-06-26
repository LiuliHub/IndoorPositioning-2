import numpy as np
from transformations import *

def GetTranslationMatrix(C):
    return np.array([[1,0,0,-C[0]],
                    [0,1,0,-C[1]],
                    [0,0,1,-C[2]],
                    [0,0,0,1]])

def GetRotationMatrix(x,y,z):
        d2r=np.pi/180
        thx=x*d2r
        thy=y*d2r 
        thz=z*d2r
        Rx=np.array([[1, 0, 0, 0],
             [0, np.cos(thx), np.sin(thx), 0],
             [0, -np.sin(thx),  np.cos(thx), 0],
                    [0,0,0,1]]) 
        Ry=np.array([[np.cos(thy), 0, -np.sin(thy), 0],
             [0, 1, 0, 0],
             [np.sin(thy), 0, np.cos(thy), 0],
                    [0,0,0,1]])
        Rz=np.array([[np.cos(thz), np.sin(thz), 0, 0],
             [-np.sin(thz),  np.cos(thz), 0, 0],
             [0, 0, 1, 0],
                    [0,0,0,1]])
        R = Rz.dot(Ry.dot(Rx))
        return np.linalg.inv(R)
        #return R

Center =[75,75,600]
D = GetTranslationMatrix(Center)
R = GetRotationMatrix(90,0,90)
T = D.dot(R)
scale, shear, angles, trans, persp = decompose_matrix(T)
print [trans[0],trans[1],trans[2]]
print np.rad2deg([angles[0],angles[1],angles[2]])