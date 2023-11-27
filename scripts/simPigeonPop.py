from pigeonSim import plumageSim
import sys

pop = plumageSim.SimulatePigeon(d=float(sys.argv[1]),tempFile=sys.argv[2])

for i in range(0,3000):
    pop.nextGen()
