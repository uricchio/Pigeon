import sys
from plumageSim import plumageSim

dx_T = float(sys.argv[1])
d = float(sys.argv[2])

for x_T in [38,41,42,43,45,48]:
    pop = plumageSim.SimulatePlumage(x_T=x_T,dx_T=dx_T,d=d)
    for i in range(1000):
        pop.nextGen()

