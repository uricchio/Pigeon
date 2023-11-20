from pigeonSim import plumageSim

pop = plumageSim.SimulatePigeon()
for i in range(0,1000):
    pop.nextGen()
