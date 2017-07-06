from src.transformations import *

M = [[  2.25744185e+02, 9.95930228e+02, 1.53361823e-08, 3.95284708e+02],[  1.69972092e+02, 4.78046509e+01, 5.27181266e-09, -2.02385770e+02],[  2.74979502e-11, 9.79614475e-11, -1.58488723e+05, 2.01139534e+03],[  0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]
scale, shear, angles, trans, persp = decompose_matrix(M)
print angles
print trans
