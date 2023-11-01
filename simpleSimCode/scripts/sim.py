from plumageSim import plumageSim

pop = plumageSim.SimulatePlumage()
for i in range(10000):
    pop.nextGen()

