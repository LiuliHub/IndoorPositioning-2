from calculate_coordinates import *
import time

s12 = 93.6
s13 = 122.1
s14 = 62.5
s23 = 50.0
s24 = 90.0
s34 = 89.4
P1M = np.array([0,0,0])
P2M = np.array([97.6,0,0])
P3M = np.array([113.1,46,0])
P4M = np.array([24.4,57.5,0])

E = Enviroment3d(s12,s13,s14,s23,s24,s34)
E.AddPointsPicture(-4.01,5.82)
E.AddPointsPicture(-2.890,5.125)
E.AddPointsPicture(-3.019,4.514)
E.AddPointsPicture(-4.132,4.979)
print "*****************************"
print "--------distancies-----------"
print E.d1()
print E.d2()
print E.d3()
print E.d4()
print "--------PC--------------------"
print E.P1C()
print E.P2C()
print E.P3C()
print E.P4C()
print "----------------T-------------"
E.Tmatrix(P1M,P2M,P3M,P4M)
#E.T = [[-0.94,0.268,-0.212,274.5],[0.240,0.959,0.148,-411,1],[0.243,0.086,-0.966,911.8],[0,0,0,1]]
print E.T
print E.GetPositonXYZ()
print "*****************************"
