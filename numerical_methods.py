import numpy as np
import math
from math import factorial
import pygame
import functools


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

            return [(xi, L(xi)) for xi in np.arange(xmin, xmax + 1, 0.1)]
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

        # calculating a 100 output points for the bezier curve
        out_pts = []
        for u in np.linspace(0, 1, 100):
            out_pts.append(P(u))
        return out_pts

    @classmethod
    def hermite(cls, pts): # just an offset lagrange now
        mylist = cls.lagrange(pts)
        mylist = [(x, y - 15) for x, y in mylist]
        return mylist
