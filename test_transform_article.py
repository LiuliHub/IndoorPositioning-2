from calculate_coordinates import *
import numpy as np

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

P1f=[qc[0][0], qc[1][0]]
P2f=[qc[0][1], qc[1][1]]
P3f=[qc[0][2], qc[1][2]]
P4f=[qc[0][3], qc[1][3]]

E = Enviroment3d(s12,s13,s14,s23,s24,s34)
E.AddPointsTest([P1f,P2f,P3f,P4f])
E.Tmatrix(P1,P2,P3,P4)
result = E.GetPositonXYZ()
TT = E.T.T
o = np.array([[0],[0],[0],[1]])

print np.matmul(o.T,np.linalg.inv(TT))[:2]
print np.rad2deg(result[3:])