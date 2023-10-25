from plumageSim import plumageSim

pop = plumageSim.SimulatePlumage()

for i in range(1000):
    pop.nextGen()
