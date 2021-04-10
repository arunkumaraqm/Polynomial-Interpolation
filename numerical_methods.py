import numpy as np
import math
import pygame


class NumericalMethods:
    @classmethod
    def lagrange(cls, pts):
        k = len(pts) - 1

        def lj_of_x(j, x):
            ret = 1

            for m in range(0, k + 1):
                xm = pts[m][0]
                xj = pts[j][0]

                if m != j:
                    ret *= (x - xm) / (xj - xm)  # fix divide by zero

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

    # bezier and hermite are just lagrange with offsets for now
    @classmethod
    def bezier(cls, pts):
        # mylist = cls.lagrange(pts)
        # mylist = [(x, y + 15) for x, y in mylist]
        # return mylist

        k = len(pts) - 1
        f_pts = []

        for n in np.arange(0, 1, 0.01):
            pt = np.zeros(2)
            for i in range(len(pts)):
                pt += np.dot(
                    (math.factorial(k) / (math.factorial(i) * math.factorial(k - i))) * ((1 - n) ** (k - i)) * (n ** i),
                    pts[i])
                f_pts.append((pt[0].astype(int), pt[1].astype(int)))
        print(f_pts)
        return f_pts

    @classmethod
    def hermite(cls, pts):
        mylist = cls.lagrange(pts)
        mylist = [(x, y - 15) for x, y in mylist]
        return mylist
