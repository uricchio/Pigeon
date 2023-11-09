from plumageSim import plumageSim

pop = plumageSim.SimulatePlumage()
pop.getSkewNormal()
for i in range(20,50):
    print (i,pop.TotalDgTmax(i))

