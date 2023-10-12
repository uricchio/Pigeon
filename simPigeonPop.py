from pigeonSim import PigeonClimate

pop = PigeonClimate.SimulatePigeon()

for i in range(500):
    pop.nextGen()
