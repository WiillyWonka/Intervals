import scipy.optimize as opt
from tolsolvty import tolsolvty
import numpy as np
import matplotlib.pyplot as plt

A = np.array([[2, 3, 4], [2.2, 3, 4], [9, 0, 0]])
infb = np.array([[2], [7], [-1]])
supb = np.array([[4], [9], [1]])
#[tolmax, argmax, envs, ccode] = tolsolvty(A, A, infb, supb)
c = [0, 0, 0, 1, 1, 1]
C = [[-2, -3, -4, -1, 0, 0],
    [-2.2, -3, -4, 0, -1, 0],
    [-9, 0, 0, 0, 0, -1],
    [2, 3, 4, -1, 0, 0],
    [2.2, 3, 4, 0, -1, 0],
    [9, 0, 0, 0, 0, -1]]
r = [-3, -8, 0, 3, 8, 0]

bounds = ((0.5, None), (None, None), (None, None), (None, None), (None, None), (None, None))
res = opt.linprog(c, A_ub=C, b_ub=r, bounds=bounds, method='interior-point')
print('Interior-point:')
print('x: (' + str(np.around(res.x[0],decimals=4)) + ',' + str(np.around(res.x[1], decimals=4))
      + ',' + str(np.around(res.x[2], decimals=4)) + ')')
print('w: (' + str(np.around(res.x[3], decimals=4)) + ',' + str(np.around(res.x[4], decimals=4))
      + ',' + str(np.around(res.x[5], decimals=4)) + ')')

bounds = ((0.5, None), (None, None), (None, None), (None, None), (None, None), (None, None))
res_simpl = opt.linprog(c, A_ub=C, b_ub=r, bounds=bounds, method='simplex')
print('Simplex:')
print('x: (' + str(res_simpl.x[0]) + ',' + str(res_simpl.x[1]) + ',' +
      str(np.around(res_simpl.x[2], decimals=4)) + ')')
print('w: (' + str(res_simpl.x[3]) + ',' + str(np.around(res_simpl.x[4], decimals=4)) + ','
      + str(np.around(res_simpl.x[5], decimals=4)) + ')')
