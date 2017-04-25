#f of camera
f=1

#Camera coordinates with respect to the world
c=np.array([[1],[1],[10]])

#Point coordinates
v=np.array([[2],[2],[1]])

d2r=pi/180

#Arbitrary rotation on x axis
thx=90*d2r
Rx=np.array([[1, 0, 0],
             [0, np.cos(thx), -np.sin(thx)],
             [0, np.sin(thx),  np.cos(thx)]])

#Arbitrary rotation on y axis
thy=90*d2r
Ry=np.array([[np.cos(thy), 0, np.sin(thy)],
             [0, 1, 0],
             [-np.sin(thy), 0, np.cos(thy)]])

#Arbitrary rotation on z axis
thz=90*d2r
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

