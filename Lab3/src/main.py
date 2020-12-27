import numpy as np
from matplotlib import cm
from matplotlib.pyplot import figure, savefig, show
from mpl_toolkits.mplot3d import Axes3D
from tolsolvty import tolsolvty

def Tol(x, infA, supA, infb, supb):
    Ac = 0.5 * (infA + supA)
    Ar = 0.5 * (supA - infA)
    bc = 0.5 * (infb + supb)
    br = 0.5 * (supb - infb)

    absx = abs(x)

    Acx = Ac @ x
    Arabsx = Ar @ absx

    infs = bc - (Acx - Arabsx)
    sups = bc - (Acx + Arabsx)

    tt = (br - np.maximum(abs(infs), abs(sups)))

    mc = np.argmin(tt)
    return  tt[mc]
    

def main():

    infA = np.array([[12,11], [16, 18], [15, 6]])
    supA = np.array([[16, 15], [20, 24], [17, 8]])
    infb = np.array([[3], [4], [2]])
    supb = np.array([[6], [8], [6]])

    '''
    infA = np.array([[12, 16, 15], [11, 18, 6]])
    supA = np.array([[16, 20, 17], [15, 24, 8]])
    infb = np.array([[7], [5]])
    supb = np.array([[12], [9]])
    '''
    [tolmax, argmax, envs, ccode] = tolsolvty(infA, supA, infb, supb)
    print('tolmax = ', tolmax)
    print('argmax = ', argmax)
    print('envs = ', envs)
    print('ccode = ', ccode)

    x = np.arange(-0.2, 1.4, 0.01)
    y = np.arange(-1.2, 0.4, 0.01)
    X, Y = np.meshgrid(x, y)
    z = np.zeros((x.shape[0], x.shape[0]))

    for i in range(sh):
        for j in range(sh):
            arr = np.array([[x[i]], [y[j]]])
            z[i, j] = Tol(arr, infA, supA, infb, supb)

    fig = figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, z, cmap=cm.coolwarm, shade=True)
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('Tol(X)')
    savefig('Tol(X)', format='png')
    show()




if __name__ == "__main__":
    main()