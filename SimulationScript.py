# %load SimulationScript.py
# %load SimulationScript.py
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from math import e

import scipy
from scipy import stats

#initial proportion of dark ("melanistic")phenotype at 44ºN
p0 = 0.20
q0 = (1-p0)


#initial population size
Ninitial = 1000
generations = 100

initial_counts = np.random.multinomial(Ninitial, [((p0)**2),(2*p0*q0), (q0**2)], size = 1)

initial_freq = (initial_counts[0][0]*2. + initial_counts[0][1])/(2.*sum(initial_counts[0]))

freqs = [initial_freq] 

def main(fileName):
    year = 2005
    climDataExtreme = loadClimExtreme(fileName)
    r_mu1, r_mu2, r_mu3 = mortalityCalc(44, climDataExtreme, year)
    return_p = nextgen(initial_freq, r_mu1, r_mu2 , r_mu3)
    for i in range(len(climDataExtreme)):
        year = year +1
        r_mu1, r_mu2, r_mu3 = mortalityCalc(44, climDataExtreme, year)
        return_p = nextgen(return_p, r_mu1, r_mu2 , r_mu3)
        freqs.append(return_p)
    
    x = range(len(climDataExtreme)+1)
    plt.plot(x, freqs)
    plt.axis([0, 97, 0, 1]);#define the plotting range
    plt.xlabel("generation")
    plt.ylabel("allele frequency")
    #print(freqs)
    

def nextgen(p, mu1, mu2 , mu3):
    #calculate number of each type of individuals in next gen after selection based on mu (mortality rate)
    #p = frequency of dark alleles in last generation
    #to add selection i would multiply the frequency of dark homozygous individuals by 
    
    type1 = (p**2)*(mu1)*Ninitial
    type2 = (2*p*(1-p))*(mu2)*Ninitial
    type3 = ((1-p)**2)*(mu3)*Ninitial
    
    #frequencies of alleles after selection
    p1 = ((2*type1)+type2)/(2*(type1 +type2 + type3))
    q1 = 1-p1
    #calculate frequency of genotypes in next generation (based on numbers after selection)
    #print("hello")
    nextCount = np.random.multinomial(Ninitial, [((p1)**2),(2*p1*q1), (q1**2)], size = 1)[0]
    p2 = (nextCount[0]*2. + nextCount[1])/(2.*sum(nextCount))
    
    return p2

def loadClimExtreme(fileName):
    climDataExtreme = []
    fh = open(fileName)
    data = fh.readlines()
    small_arr = []
    for item in data:
        small_arr = item.split(',')
        small_arr[1] = small_arr[1].replace("\n", "")
        small_arr[1] = small_arr[1].replace("\r", "")
#         if float(item[1]) != 0.0:
        climDataExtreme.append(small_arr)
    return(climDataExtreme) 

#can either modify temp experienced for each group
#new mu values equal to functions of temp
def mortalityCalc(latitude, climDataExtreme, year):
#initialize variables (weight in g)
    airTempF = 105
    airTempC = (airTempF-32.0)*(5.0/9.0)
    baselineWeight = 296.67
#pull in days over air temp from climate data
    days = 0
    for item in climDataExtreme:
        if item[0] == str(year):
            days = float(item[1])
    #print(days)
#mortality rates (mu = (1-x)^days)
#x = mortality
#air temp to body temp (one for each group? 1 2 and 3 will experience different body temps for the same air temp)
#the data that these equations are based on does not specify the colors of the pigeons used
#0.5 is from "pigeons in the sun"
    bodyTemp1 = 34.2297 + (airTempC)*0.1789 +0.5
    bodyTemp2 = 34.2297 + (airTempC)*0.1789 +0.5
    bodyTemp3 = 34.2297 + (airTempC)*0.1789
#body temp to EWL
#EWL updated to be per 5 hours
#baseline pigeon weight and proportion of weight lost
    EWL1 = -417.19 + (bodyTemp1)*10.45 
    EWL2 = -417.19 + (bodyTemp2)*10.45
    EWL3 = -417.19 + (bodyTemp3)*10.45
    #print(EWL1,EWL2,EWL3)
    
#baseline pigeon weight = 297.67 (average weight from ovocontrol website)
    prop1 = (baselineWeight-EWL1)/baselineWeight
    prop2 = (baselineWeight-EWL2)/baselineWeight
    prop3 = (baselineWeight-EWL3)/baselineWeight
#find correspoding point on mortality curve = per day mortality
#normal pigeon mortality is 30% (ovocontrol) 
    x1 = 1.0-0.0006319*(e**(22.08*(prop1)**2.0))
    x2 = 1.0-0.0006319*(e**(22.08*(prop2)**2.0))
    x3 = 1.0-0.0006319*(e**(22.08*(prop3)**2.0))
    #print(x1,x2,x3)
    
#surivival prob per year
    mu1 = (1.0-x1)**days
    mu2 = (1.0-x2)**days
    mu3 = (1.0-x3)**days
    #print(mu1,mu2,mu3)
    return mu1, mu2, mu3