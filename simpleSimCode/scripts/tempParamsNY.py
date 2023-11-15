from plumageSim import plumageSim

pop = plumageSim.SimulatePlumage(tempFile="/Users/uricchio/projects/Pigeon/tempData/Manhattan.GHCND:USW00094728.tMax.csv")
pop.getSkewNormal(prParams=True)

