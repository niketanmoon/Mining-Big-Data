import numpy as np 
from fractions import Fraction
M = np.matrix([
    [0, Fraction(1, 2), 0, 0],
    [Fraction(1, 3), 0, 0, Fraction(1, 2)],
    [Fraction(1, 3), 0, 1, Fraction(1, 2)],
    [Fraction(1, 3), Fraction(1, 2), 0, 0]
])

# Number of nodes
n = M.shape[0]

# an initial column vector with 1/n value
v = np.zeros((n, 1)) + 1./n

E = np.ones((n, 1))

beta = 0.8

ep = 1./10**10

for _ in range(1, 100):
    new_v = beta*M*v + (1-beta)*E/n
    if np.sum(np.abs(new_v - v)) < ep:
        break
    v = new_v


v = v / np.sum(v)
for idx, val in enumerate(v):
    print(idx, val[0])

