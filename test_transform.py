
import numpy as np
from src.transformations import *
from src.calculate_coordinates import *
from src.frameV2 import *

#Camera coordinates with respect to the world
c=np.array([[50],[50],[900]])
rot = np.array([180,0,90])



#Point coordinates
#v=np.array([[0],[0],[0]])
p1=np.array([0,0,0]);
p2=np.array([40,0,0]);
p3=np.array([40,100,0]);
p4=np.array([0,100,0]);
v=np.vstack((p1,p2,p3,p4));
v=v.T;

d2r=np.pi/180

#Arbitrary rotation of camera on x axis. 
#Axes are always WORLD axes. They do not change with the object
thx=rot[0]*d2r
Rx=np.array([[1, 0, 0],
             [0, np.cos(thx), -np.sin(thx)],
             [0, np.sin(thx),  np.cos(thx)]])

#Arbitrary rotation on y axis
thy=rot[1]*d2r
Ry=np.array([[np.cos(thy), 0, np.sin(thy)],
             [0, 1, 0],
             [-np.sin(thy), 0, np.cos(thy)]])

#Arbitrary rotation on z axis
thz=rot[2]*d2r
Rz=np.array([[np.cos(thz), -np.sin(thz), 0],
             [np.sin(thz),  np.cos(thz), 0],
             [0, 0, 1]])
R=Rz.dot(Ry.dot(Rx))

# v-c :final vector minus initial vector)
#      This is the point seen from the camera coordinates
# without rotation
# 

vc=R.dot(v-c) # includes rotation
f = 3.6
qc=vc*1.0*f/(vc[2])

def distance(Pi,Pj):
            return np.sqrt( np.abs(Pi[0]-Pj[0])**2.0 + np.abs(Pi[1]-Pj[1])**2.0 + np.abs(Pi[2]-Pj[2])**2.0 )
P1 = [0,0,0]
P4 = [0,100,0]
P2 = [40,0,0]
P3 = [40,100,0]

s12 = distance(P1,P2) 
s13 = distance(P1,P3)
s14 = distance(P1,P4)
s23 = distance(P2,P3)
s24 = distance(P2,P4)
s34 = distance(P3,P4)



#Pixel diference
PX = ( 1944 * 1.4*10**(-3))/384
PY = ( 2592 * 1.4*10**(-3))/512
frame = Frame()
xmin=384/2*PX
ymax=512/2*PX

P1f=[qc[0][0], qc[1][0]]
P2f=[qc[0][1], qc[1][1]]
P3f=[qc[0][2], qc[1][2]]
P4f=[qc[0][3], qc[1][3]]

P1fd=[qc[0][0], qc[1][0]]
P2fd=[qc[0][1]+PX, qc[1][1]]
P3fd=[qc[0][2], qc[1][2]]
P4fd=[qc[0][3], qc[1][3]]

D1 = Enviroment3d(s12,s13,s14,s23,s24,s34)
D1.AddPointsTest([P1f,P2f,P3f,P4f])
D1.Tmatrix(P1,P2,P3,P4)
result = D1.GetPositonXYZ()
print D1.IsAGoodMesurement()

D2 = Enviroment3d(s12,s13,s14,s23,s24,s34)
Points2 = [P1fd,P2fd,P3fd,P4fd]
FPoints2 = frame.CheckCenters(Points2)
D2.AddPointsTest([P1fd,P2fd,P3fd,P4fd])
D2.Tmatrix(P1,P2,P3,P4)
result2 = D2.GetPositonXYZ()
print D2.IsAGoodMesurement()

print D2.AblePrintDistance()

'''
print str([qc[0][0], qc[1][0]]) +' to '+ str([qc[0][0] +PX, qc[1][0]])
print str([qc[0][1], qc[1][1]]) +' to '+ str([qc[0][1], qc[1][1]])
print str([qc[0][2], qc[1][2]]) +' to '+ str([qc[0][2], qc[1][2]])
print str([qc[0][3], qc[1][3]]) +' to '+ str([qc[0][3], qc[1][3]])
'''
print "**************************"
print "Distance 1: "+str(D2.d1)+"     "+str(D1.d1)
print "Distance 2: "+str(D2.d2)+"     "+str(D1.d2)
print "Distance 3: "+str(D2.d3)+"     "+str(D1.d3)
print "Distance 4: "+str(D2.d4)+"     "+str(D1.d4)
print "X0 = "+str(result[0])+"          "+str(result2[0])
print "Y0 = "+str(result[1])+"          "+str(result2[1])
print "Z0 = "+str(result[2])+"          "+str(result2[2])
print "a = "+str(np.rad2deg(result[3]))+"  "+str(np.rad2deg(result2[3]))+"     "
print "b = "+str(np.rad2deg(result[4]))+"  "+str(np.rad2deg(result2[4]))+"     "
print "c = "+str(np.rad2deg(result[5]))+"  "+str(np.rad2deg(result2[5]))+"     "
print "**************************"
