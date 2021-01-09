import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import random

def plot_solutions(Ax_inf, Ax_sup, b_inf, b_sup, b_real, filename=''):
    plt.figure()
    plt.plot(Ax_sup, label='A * x_sup')
    plt.plot(Ax_inf, label='A * x_inf')
    plt.plot(b_sup, label='b_sup', ls='--')
    plt.plot(b_inf, label='b_inf', ls='--')
    plt.plot(b_real, label='b_real')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.legend()
    #plt.show()
    if len(filename) != 0: plt.savefig("../fig/" + filename)

def plot_xs(x_real, x_inf, x_sup, filename):
    plt.figure()
    plt.plot(x_real, label='x_real')
    plt.plot(x_sup, label='x_sup')
    plt.plot(x_inf, label='x_inf')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.legend()
    if len(filename) != 0: plt.savefig("../fig/" + filename)
    else: plt.show()

def createHeatMap(matrix, title='', filename=''):
    plt.figure(figsize=(16, 9))
    sns.heatmap(matrix, center=0)
    plt.title(title)
    if len(filename) != 0: plt.savefig("../fig/" + filename)
    else: plt.show()


def findBestMatrix(matrix, size):
    print('Task ', size, 'x', size)
    det = 0
    out_matr = []
    indexes = [i for i in range(matrix.shape[0])]
    count_iter = 50000
    for i in range(count_iter):
        cur_indexes = random.sample(indexes, size)
        cur_matr = []
        for elem in cur_indexes:
            if len(cur_matr) == 0:
                cur_matr = np.array([matrix[elem]])
            else:
                cur_matr = np.append(cur_matr, [matrix[elem]], axis=0)

        cur_det = np.linalg.det(cur_matr)
        if cur_det > det:
            det = cur_det
            out_matr = cur_matr.copy()
        if i % (count_iter / 10) == 0:
            print('Brute force progress: ', i / (count_iter / 100), '%')
            print('Current max det: ', det)

    print()
    print('Max det in find matrix :', det)
    print()
    if len(out_matr) != 0:
        return out_matr
    else:
        return matrix[:size][:size]


def createSignBlockMatrix(matrix):
    pos, neg = matrix.copy(), matrix.copy()
    pos[pos < 0] = 0
    neg[neg > 0] = 0
    neg = np.abs(neg)
    return np.block([[pos, neg], [neg, pos]])


def calcD(D, i, j, cur_interval, b_inf, b_sup):
    size = int(D.shape[0] / 2)

    a_inf = cur_interval[0]
    a_sup = cur_interval[1]

    k = 0
    m = 0
    if a_inf * a_sup > 0:
        k = 0 if a_inf > 0 else 2
    else:
        k = 1 if a_inf < a_sup else 3

    if b_inf * b_sup > 0:
        m = 1 if b_inf > 0 else 3
    else:
        m = 2 if b_inf <= b_sup else 4

    case = 4 * k + m
    if case == 1:
        D[i][j] = a_inf
        D[i + size][j + size] = a_sup
    elif case == 2:
        D[i][j] = a_sup
        D[i + size][j + size] = a_sup
    elif case == 3:
        D[i][j] = a_sup
        D[i + size][j + size] = a_inf
    elif case == 4:
        D[i][j] = a_inf
        D[i + size][j + size] = a_inf
    elif case == 5:
        D[i][j + size] = a_inf
        D[i + size][j + size] = a_sup
    elif case == 6:
        if a_inf * b_sup < a_sup * b_inf:
            D[i][j + size] = a_inf
        else:
            D[i][j] = a_sup
        if a_inf * b_inf > a_sup * b_sup:
            D[i + size][j] = a_inf
        else:
            D[i + size][j + size] = a_sup
    elif case == 7:
        D[i][j] = a_sup
        D[i + size][j] = a_inf
    elif case == 8:
        return D
    elif case == 9:
        D[i][j + size] = a_inf
        D[i + size][j] = a_sup
    elif case == 10:
        D[i][j + size] = a_inf
        D[i + size][j] = a_inf
    elif case == 11:
        D[i][j + size] = a_sup
        D[i + size][j] = a_inf
    elif case == 12:
        D[i][j + size] = a_sup
        D[i + size][j] = a_sup
    elif case == 13:
        D[i][j] = a_inf
        D[i + size][j] = a_sup
    elif case == 14:
        return D
    elif case == 15:
        D[i][j + size] = a_sup
        D[i + size][j + size] = a_inf
    elif case == 16:
        if a_inf * b_inf > a_sup * b_sup:
            D[i][j] = a_inf
        else:
            D[i][j + size] = -a_sup
        if a_inf * b_sup < a_sup * b_inf:
            D[i + size][j + size] = a_inf
        else:
            D[i + size][j] = a_sup
    return D


def calcG(A, last_x, sti_vec):
    half_size = int(last_x.shape[0] / 2)
    inf, sup = -last_x[:half_size], last_x[half_size:]
    intervals = np.array([[inf[i], sup[i]] for i in range(inf.shape[0])])
    dot = [sum([A[i][j] * intervals[j] for j in range(len(intervals))]) for i in range(len(A))]
    dot_lower, dot_upper = np.array([i[0] for i in dot]), np.array([i[1] for i in dot])
    return np.append(-dot_lower, dot_upper) - sti_vec

def subdiff2(A_inf, A_sup, b_inf, b_sup, lr=0.5, acc=1e-10, max_iter=150):
    size = A_inf.shape[0]

    A = np.array([[[A_inf[i][j], A_sup[i][j]] for j in range(size)] for i in range(size)])
    A_mid = np.array([[(A_inf[i][j] + A_sup[i][j]) / 2 for j in range(size)] for i in range(size)])

    A_block = createSignBlockMatrix(A_mid)
    sti_vec = np.append(-b_inf, b_sup)
    cur_x = np.dot(np.linalg.inv(A_block), sti_vec)

    last_x = cur_x

    iter = 0
    firstStep = True
    while firstStep or np.linalg.norm(cur_x - last_x) > acc:
        firstStep = False
        iter += 1
        if iter > max_iter:
            print('Too many iterations')
            break
        last_x = cur_x
        D = np.zeros([2 * size, 2 * size])
        for i in range(size):
            for j in range(size):
                cur_interval = A[i][j]
                last_inf = -last_x[j]
                last_sup = last_x[j + size]
                D = calcD(D, i, j, cur_interval, last_inf, last_sup)
        G = calcG(A, last_x, sti_vec)
        dx = np.dot(np.linalg.inv(D), -G)
        cur_x = last_x + lr * dx

    return cur_x, iter


def task1():
    A_inf = np.array([[1, 1],
                      [0, 0.1]])

    A_sup = A_inf.copy()

    b_inf, b_sup = np.array([1.3, 1.5]), np.array([1.1, 1.8])

    sol_x, iter = subdiff2(A_inf, A_sup, b_inf, b_sup)

    middle_index = int(sol_x.shape[0] / 2)
    c_inf, c_sup = -sol_x[:middle_index], sol_x[middle_index:]

    print('Iterations: ', iter)
    print('Solution: \n', np.block([[c_inf], [c_sup]]).T)


def task2():
    file = 'matrix_n_phi_6.txt'
    A = np.loadtxt(file)
    A = A
    A = A[120:174,92:108]
    A += np.random.random(A.shape)*0.0001

    createHeatMap(A)

    size = min(A.shape)
    x = np.random.uniform(low=2, high=8,size=size)
    rad = np.random.uniform(low=0.1, high=1.5, size=size)

    A_cool = findBestMatrix(A, size)

    createHeatMap(A_cool, title="", filename="nonspecial_2")

    b = np.dot(A_cool, x)
    b_inf = b - rad
    b_sup = b + rad

    first_sol_x, iter = subdiff2(A_cool, A_cool, b_inf, b_sup)

    middle_index = int(first_sol_x.shape[0] / 2)
    x_inf, x_sup = -first_sol_x[:middle_index], first_sol_x[middle_index:]

    print('Iterations count for first matrix: ', iter)

    plot_solutions(np.dot(A_cool, x_inf), np.dot(A_cool, x_sup), b_inf, b_sup, b, filename="b_comp_2")

    plot_xs(x, x_inf, x_sup, filename="x_comp_2")

if __name__ == "__main__":
    '''
    file = 'matrix_n_phi_6.txt'
    A = np.loadtxt(file)
    createHeatMap(A, filename="matrix_2")
    '''
    task2()