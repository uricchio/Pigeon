from plumageSim import plumageSim

pop = plumageSim.SimulatePlumage()

for i in range(5000):
    pop.nextGen()
