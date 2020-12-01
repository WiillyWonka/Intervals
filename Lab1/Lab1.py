import numpy as np

class Interval:
    def __init__(self, l_bound, r_bound):
        self._l_bound = l_bound
        self._r_bound = r_bound

    def __add__(self, other):
        return Interval(self._l_bound + other._l_bound, self._r_bound + other._r_bound)

    def __sub__(self, other):
        return Interval(self._l_bound - other._r_bound, self._r_bound - other._l_bound)

    def __mul__(self, other):
        l_bound = min([self._l_bound * other._l_bound, self._l_bound * other._r_bound, \
        self._r_bound * other._l_bound, self._r_bound * other._r_bound])

        r_bound = max([self._l_bound * other._l_bound, self._l_bound * other._r_bound, \
             self._r_bound * other._l_bound, self._r_bound * other._r_bound])

        return Interval(l_bound, r_bound)

    def mid(self):
        return (self._l_bound + self._r_bound) / 2

    def rad(self):
        return  (self._r_bound - self._l_bound) / 2

    def __str__(self):
        return "(" + str(np.around(self._l_bound, decimals=5)) + ", " + str(np.around(self._r_bound, decimals=5)) + ")"

    def isContainZero(self):
        return self._l_bound <= 0 and self._r_bound >= 0

class IntervalMatrix:
    def _createFirstMatrix(self, eps):
        return np.array([[Interval(1 - eps, 1 + eps), Interval(1 - eps, 1 + eps)], \
             [Interval(1.1 - eps, 1.1 + eps), Interval(1 - eps, 1 + eps)]])

    def _createSecondMatrix(self, eps, size):
        matrix = np.array([[Interval(0, 0) for i in range(size)] for j in range(size)])
        for i in range(size):
            for j in range(size):
                if i != j:
                    matrix[i][j] = Interval(0, eps)
                else:
                    matrix[i][j] = Interval(1, 1)
        return matrix


    def __init__(self, task, eps, size = 2):
        self.size = size
        if task == 1:
            self.matrix = self._createFirstMatrix(eps)
        else:
            self.matrix = self._createSecondMatrix(eps, size)

    def mid(self):
        M = np.zeros((self.size, self.size))
        for i in range(self.size):
            for j in range(self.size):
                M[i][j] = self.matrix[i][j].mid()
        return M

    def rad(self):
        R = np.zeros((self.size, self.size))
        for i in range(self.size):
            for j in range(self.size):
                R[i][j] = self.matrix[i][j].rad()
        return R

    def det(self):
        if self.size == 2:
            return self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]
        if self.size == 3:
            return self.matrix[0][0]*self.matrix[1][1]*self.matrix[2][2] + self.matrix[2][0]*self.matrix[0][1]*self.matrix[1][2] \
                + self.matrix[1][0]*self.matrix[2][1]*self.matrix[0][2] - self.matrix[2][0]*self.matrix[1][1]*self.matrix[0][2] \
                - self.matrix[0][0]*self.matrix[2][1]*self.matrix[1][2] - self.matrix[1][0]*self.matrix[0][1]*self.matrix[2][2]


def beck(matrix):
    M = matrix.mid()
    R = matrix.rad()
    M_inv = np.linalg.inv(M)
    M_inv = np.abs(M_inv)

    A = M_inv.dot(R)
    eig = np.abs(np.linalg.eigvals(A))
    rho = np.max(eig)

    if rho < 1:
        result = 'non-special matrix'
    else:
        result = 'unknown'

    return result, rho

def diag_max(matrix):
    M = matrix.mid()
    R = matrix.rad()
    M_inv = np.linalg.inv(M)
    M_inv = np.abs(M_inv)
    A = R.dot(M_inv)

    Max = max([A[i][i] for i in range(matrix.size())])

    if Max >= 1:
        result = 'special matrix'
    else:
        result = 'unknown'

    return result, Max

if __name__ == "__main__":
    #print('Enter eps: ')
    #eps = float(input())
    eps = 1.29
    print('det =', IntervalMatrix(2, eps).det())
    
    '''
    eps = 0.048

    while IntervalMatrix(1, eps).det().isContainZero():
        eps -= 0.001

    eps += 0.001
    print ("det =", IntervalMatrix(1, eps).det())
    print("end eps =", eps)
    '''
    


