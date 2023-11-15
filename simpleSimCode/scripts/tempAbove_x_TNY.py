from plumageSim import plumageSim


for x_T in [25,28,30,33,35,38]:
    pop = plumageSim.SimulatePlumage(x_T=x_T,dx_T=2,tempFile="/Users/uricchio/projects/Pigeon/tempData/Manhattan.GHCND:USW00094728.tMax.csv")
    pop.getdA_minus_da()

