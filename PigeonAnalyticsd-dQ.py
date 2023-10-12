import math
import mpmath
import numpy as np

# a script to calculate values for plots in Wright-Lichter et al 2023

def qEq(sa, Sa, sA, SA):
    if sa + sA == 0:
        return np.nan
    if (sA-Sa+SA)/(sa+sA) > 0:
        return ((sA-Sa+SA)/(sa+sA))**0.5
    return np.nan

def fitness(S,s,x):
    return S + s*x

def delta_q(q,sa,Sa,sA,SA):
    num =  q**2 * fitness(Sa,sa,q**2) + q * (1-q) * fitness(SA,sA,1-q**2)
    den = q**2 * fitness(Sa,sa,q**2)+(1-q**2)*fitness(SA,sA,1-q**2)
    return num/den - q

def dDelQ(sa,Sa,sA,SA):
    num =- 2*(sa+sA)**2 * (qEq(sa, Sa, sA, SA)**3) * (qEq(sa, Sa, sA, SA)-1)
    den = sA*Sa + sa*(sA+SA)
    return num/den

# negative frequency dependence
for sa in np.arange(-0.01,0.01,0.0001):
    feas = qEq(sa,0.992,-0.01,1)
    if feas > 0 and feas < 1:
        feas = 1
    else:
        feas = 2
    print(dDelQ(sa,1,-0.01,1),sa,-0.01,1,feas)

#positive frequency dependence
for sa in np.arange(-0.01,0.01,0.0001):
    feas = qEq(sa,1,0.01,1)
    if feas > 0 and feas < 1:
        feas = 1
    else:
        feas = 2
    print(dDelQ(sa,1,0.01,1),sa,0.01,1,feas)

# negative dependence, recessive weaker
for sa in np.arange(-0.01,0.01,0.0001):
    feas = qEq(sa,0.995,-0.01,1)
    if feas > 0 and feas < 1:
        feas = 1
    else:
        feas = 2
    print(dDelQ(sa,0.995,-0.01,1),sa,-0.01,0.995,feas)

for sa in np.arange(-0.01,0.01,0.0001):
    feas = qEq(sa,0.992,-0.01,1)
    if feas > 0 and feas < 1:
        feas = 1
    else:
        feas = 2
    print(dDelQ(sa,0.992,-0.01,1),sa,-0.01,0.992,feas)


