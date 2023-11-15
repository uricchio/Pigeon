from plumageSim import plumageSim


for x_T in [38,41,42,43,45,48]:
    pop = plumageSim.SimulatePlumage(x_T=x_T,dx_T=2)
    pop.getdA_minus_da()

