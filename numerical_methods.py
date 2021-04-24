import numpy as np
import math
from math import factorial
import functools

# import matplotlib.pyplot as plt

# prolly wise to memoize
def nCk(n, k):
    numerator = factorial(n)
    denominator = factorial(k) * factorial(n - k)
    return numerator/denominator

class NumericalMethods:
    @classmethod
    def lagrange(cls, pts):
        k = len(pts) - 1

        # Lagrange polynomials are not defined when any two of the x coords over the set of points are the same
        if len(set(pt[0] for pt in pts)) < len(pts):
            raise ValueError('Lagrange polynomial cannot be defined.')

        def lj_of_x(j, x):
            ret = 1

            for m in range(0, k + 1):
                xm = pts[m][0]
                xj = pts[j][0]

                if m != j:
                    denom = xj - xm
                    ret *= (x - xm) / denom 

            return ret

        def L(x):
            summ = 0
            for j in range(0, k + 1):
                yj = pts[j][1]
                summ += yj * lj_of_x(j, x)
            return summ

        if len(pts):
            xmin = min(pts, key=lambda pt: pt[0])[0]
            xmax = max(pts, key=lambda pt: pt[0])[0]

            return [(xi, L(xi)) for xi in np.arange(xmin, xmax + 1, 0.01)]
        else:
            return []

    @classmethod
    def bezier(cls, pts):
        # formula taken from hearn, baker, carithers pg 422/429
                
        points = np.array(pts)

        def P(u):
            summ = np.array([0, 0], dtype = 'float')
            n = len(points) - 1
            for k in range(0, n + 1):
                prod = points[k] * nCk(n, k) * u ** k * (1-u) ** (n-k)
                summ += prod
            return summ

        # calculating a 1000 output points for the bezier curve
        out_pts = []
        for u in np.linspace(0, 1, 1000):
            out_pts.append(P(u))
        return out_pts

    @classmethod
    def cardinal(cls, pts): 
        if len(pts) < 4:
            raise ValueError('Insufficient points for Cardinal spline.')

        t = 0 # this Cardinal spline is an Overhauser spline
        s = (1 - t) / 2

        cardinal_matrix = np.array([
            [-s,        2 - s,          s - 2,      s],
            [2 * s,     s - 3,      3 - 2 * s,      -s],
            [-s,            0,              s,      0],
            [0,             1,              0,      0]
        ])

        def P(iu, out_pts):
            pos_u, u = iu
            ret = np.array([u**3, u**2, u, 1]).reshape([1, 4])
            ret = np.matmul(ret, cardinal_matrix)

            modified_pts = pts[-1:] + pts + pts[:2]
            for k in range(len(pts)):
                four_pts = np.array([
                    modified_pts[k], # p_k-1
                    modified_pts[k + 1], # p_k
                    modified_pts[k + 2], #p_k+1
                    modified_pts[k + 3], #p_k+2
                ]).reshape([4, 2])
                out_pts[k,pos_u,:] = np.matmul(ret, four_pts)

        nf_pieces_per_pair = 100
        out_pts = np.zeros([len(pts), nf_pieces_per_pair, 2])
        for i, u in enumerate(np.linspace(0, 1, nf_pieces_per_pair)): P((i, u), out_pts)

        out_pts = out_pts.reshape(len(pts) * nf_pieces_per_pair, 2)
        # plt.scatter(out_pts[:,0], out_pts[:, 1], color='blue')
        # pts = np.array(pts)
        # plt.scatter(pts[:,0], pts[:, 1], color='red')
        # plt.show()

        return out_pts

if __name__ == '__main__':

    ## figure 16
    # NumericalMethods.cardinal([
    #     [0, 0],
    #     [3, 6],
    #     [7, 6],
    #     [10, 0],
    # ])

    ## figure 17
    # NumericalMethods.cardinal([
    #     [0, 0],
    #     [5, 6],
    #     [5, 6],
    #     [10, 0],
    # ])

    ## figure 18
    # NumericalMethods.cardinal([
    #     [0, 0],
    #     [4.9, 6],
    #     [5.1, 6],
    #     [10, 0],
    # ])
    pass