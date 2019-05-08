from itertools import chain
from cvxopt import blas, lapack, solvers
from cvxopt import matrix, spmatrix, sin, mul, div, normal, spdiag
solvers.options['show_progress'] = 0



def get_second_derivative_matrix(n):
    """
    :param n: The size of the time series

    :return: A matrix D such that if x.size == (n,1), D * x is the second derivate of x
    """
    m = n - 2
    D = spmatrix(list(chain(*[[1, -2, 1]] * m)),
                 list(chain(*[[i] * 3 for i in range(m)])),
                 list(chain(*[[i, i + 1, i + 2] for i in range(m)])))
    return D


def _l1tf(corr, delta):
    """
        minimize    (1/2) * ||x-corr||_2^2 + delta * sum(y)
        subject to  -y <= D*x <= y

    Variables x (n), y (n-2).

    :param x:
    :return:
    """

    n = corr.size[0]
    m = n - 2

    D = get_second_derivative_matrix(n)

    P = D * D.T
    q = -D * corr

    G = spmatrix([], [], [], (2*m, m))
    G[:m, :m] = spmatrix(1.0, range(m), range(m))
    G[m:, :m] = -spmatrix(1.0, range(m), range(m))

    h = matrix(delta, (2*m, 1), tc='d')

    res = solvers.qp(P, q, G, h)

    return corr - D.T * res['x']
