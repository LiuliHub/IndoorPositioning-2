#Camera coordinates with respect to the world
c=np.array([[1],[1],[10]])

#Point coordinates
v=np.array([[2],[2],[1]])

#Rotation
R=np.array([[-1, 0, 0],[0, 1, 0],[0, 0, -1]])

# v-c :final vector minus initial vector)
#      This is the point seen from the camera coordinates
# without rotation
# 

vc=R.dot(v-c) # includes rotation

#Compute intersection with the plane z=f
qc=vc*1.0*f/(vc[2])

