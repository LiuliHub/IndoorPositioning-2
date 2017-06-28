import numpy as np
"""
Given a set of points p1..p4
Find how they are seen by a camera

The camera is situated at c
The camera is first rotated thx around the world x axis
Then it is rotated thy around the world (not the local) y axis
Then it is rotated thz around the world z axis

The focal length of the camera is f
"""

#f of camera
f=1

#Camera coordinates with respect to the world
c=np.array([[10],[10],[100]])

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
thx=180*d2r
Rx=np.array([[1, 0, 0],
             [0, np.cos(thx), -np.sin(thx)],
             [0, np.sin(thx),  np.cos(thx)]])

#Arbitrary rotation on y axis
thy=0*d2r
Ry=np.array([[np.cos(thy), 0, np.sin(thy)],
             [0, 1, 0],
             [-np.sin(thy), 0, np.cos(thy)]])

#Arbitrary rotation on z axis
thz=85*d2r
Rz=np.array([[np.cos(thz), -np.sin(thz), 0],
             [np.sin(thz),  np.cos(thz), 0],
             [0, 0, 1]])
R=Rz.dot(Ry.dot(Rx))

# v-c :final vector minus initial vector)
#      This is the point seen from the camera coordinates
# without rotation
# 

vc=R.dot(v-c) # includes rotation

#Compute intersection with the plane z=f
qc=vc*1.0*f/(vc[2])

