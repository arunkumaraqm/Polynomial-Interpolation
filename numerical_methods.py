import numpy as np

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
					ret *= (x - xm)/(xj - xm) # fix divide by zero

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
		mylist = cls.lagrange(pts)
		mylist = [(x, y + 15) for x, y in mylist]
		return mylist

	@classmethod
	def hermite(cls, pts):
		mylist = cls.lagrange(pts)
		mylist = [(x, y - 15) for x, y in mylist]
		return mylist
