import numpy as np
from transformations import *
from calculate_coordinates import *

#Camera coordinates with respect to the world
c=np.array([[50],[50],[400]])
rot = np.array([175,0,75])



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

xmin=384/2*PX
ymax=512/2*PX

P1f=[qc[0][0], qc[1][0]]
P2f=[qc[0][1]+1*PX, qc[1][1]]
P3f=[qc[0][2], qc[1][2]]
P4f=[qc[0][3], qc[1][3]]

E = Enviroment3d(s12,s13,s14,s23,s24,s34)
E.AddPointsTest([P1f,P2f,P3f,P4f])
E.Tmatrix(P1,P2,P3,P4)
result = E.GetPositonXYZ()
TT = E.T.T
o = np.array([[0],[0],[0],[1]])

print str([qc[0][0], qc[1][0]]) +' to '+ str([qc[0][0] +PX, qc[1][0]])
print str([qc[0][1], qc[1][1]]) +' to '+ str([qc[0][1], qc[1][1]])
print str([qc[0][2], qc[1][2]]) +' to '+ str([qc[0][2], qc[1][2]])
print str([qc[0][3], qc[1][3]]) +' to '+ str([qc[0][3], qc[1][3]])

print "**************************"
print "X0 = "+str(np.matmul(o.T,np.linalg.inv(TT))[0][0])
print "Y0 = "+str(np.matmul(o.T,np.linalg.inv(TT))[0][1])
print "Z0 = "+str(np.matmul(o.T,np.linalg.inv(TT))[0][2])
print "a = "+str(np.rad2deg(result[3]))
print "b = "+str(np.rad2deg(result[4]))
print "c = "+str(np.rad2deg(result[5]))
print "**************************"
