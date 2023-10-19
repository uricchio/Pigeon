import math
import mpmath
import numpy as np

# a script to calculate values for plots in Wright-Lichter et al 2023

def qEq(sa, Sa, sA, SA):
    return ((sA-Sa+SA)/(sa+sA))**0.5

def fitness(S,s,x):
    return S + s*x

def delta_q(q,sa,Sa,sA,SA):
    numerator =  q**2 * fitness(Sa,sa,q**2) + q * (1-q) * fitness(SA,sA,1-q**2)
    denominator = q**2 * fitness(Sa,sa,q**2)+(1-q**2)*fitness(SA,sA,1-q**2)
    return numerator/denominator - q

# negative frequency dependence
for q in np.arange(0,1,0.001):
    print(delta_q(q,-0.01,1,-0.01,1),q,-0.01,1)  

#positive frequency dependence
for q in np.arange(0,1,0.001):
    print(delta_q(q,0.01,1,0.01,1),q,0.01,1)  

# negative dependence, recessive weaker
for q in np.arange(0,1,0.001):
    print(delta_q(q,-0.01,0.995,-0.01,1),q,-0.01,0.995)  

for q in np.arange(0,1,0.001):
    print(delta_q(q,-0.01,0.992,-0.01,1),q,-0.01,0.992)  

