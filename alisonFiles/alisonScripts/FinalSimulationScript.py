# %load SimulationScript.py
# %load SimulationScript.py
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from math import e
from math import sqrt


import scipy
from scipy import stats


Ninitial = 1000

def main(fileName):
    latData = loadLat()
    latitude = citytoLat(fileName, latData)
    print(latitude)
    
    p0, q0 = calcP(latitude)
    print(p0,q0)

    initial_counts = np.random.multinomial(Ninitial, [((p0)**2),(2*p0*q0), (q0**2)], size = 1)

    initial_freq = (initial_counts[0][0]*2. + initial_counts[0][1])/(2.*sum(initial_counts[0]))

    freqs = [initial_freq] 
    
    year = 2005
    climDataExtreme = loadClimExtreme(fileName)
    r_mu1, r_mu2, r_mu3 = mortalityCalc(climDataExtreme, year)
    return_p = nextgen(initial_freq, r_mu1, r_mu2 , r_mu3)
    for i in range(len(climDataExtreme)):
        year = year +1
        r_mu1, r_mu2, r_mu3 = mortalityCalc(climDataExtreme, year)
        return_p = nextgen(return_p, r_mu1, r_mu2 , r_mu3)
        freqs.append(return_p)
    
    x = range(2004,2101)
    plt.plot(x, freqs)
    plt.axis([2005, 2099, 0, 0.3]);#define the plotting range
    plt.xlabel("year")
    plt.ylabel("allele frequency")

#function to go from the city name provided, to its latitude
def citytoLat(fileName, latData):
    cityName = fileName.replace(".csv","")
    latitude = 0
    for item in latData:
        if item[0] == str(cityName):
            latitude = float(item[1])
    return latitude
    
#function to calculate proportion of dark ("melanistic")phenotype
def calcP(latitude):
    #equation comes from data source: Obukhova, N.Y. Dynamics of balanced polymorphism morphs in blue rock pigeon                           Columbia livia . Russ J Genet 47, 83–89 (2011). https://doi.org/10.1134/S1022795411010078
    p0 =  -0.125208 + (0.005787*latitude)
    
    p = 1-sqrt((-p0)+1)
    q = (1-p)
    return p, q

def nextgen(p, mu1, mu2 , mu3):
    #calculate number of each type of individuals in next gen after selection based on mu (mortality rate)
    #p = frequency of dark alleles in last generation
    #add selection -> multiply the frequency of dark homozygous individuals by initial population and mu
    
    type1 = (p**2)*(mu1)*Ninitial
    type2 = (2*p*(1-p))*(mu2)*Ninitial
    type3 = ((1-p)**2)*(mu3)*Ninitial
    
    #frequencies of alleles after selection
    p1 = ((2*type1)+type2)/(2*(type1 +type2 + type3))
    q1 = 1-p1
    #calculate frequency of genotypes in next generation (based on numbers after selection)
    nextCount = np.random.multinomial(Ninitial, [((p1)**2),(2*p1*q1), (q1**2)], size = 1)[0]
    p2 = (nextCount[0]*2. + nextCount[1])/(2.*sum(nextCount))
    
    return p2

#climate data source: https://crt-climate-explorer.nemac.org/
def loadClimExtreme(fileName):
    climDataExtreme = []
    fileName = fileName
    fh = open(fileName)
    data = fh.readlines()
    small_arr = []
    for item in data:
        small_arr = item.split(',')
        small_arr[1] = small_arr[1].replace("\n", "")
        small_arr[1] = small_arr[1].replace("\r", "")
        climDataExtreme.append(small_arr)
    return(climDataExtreme) 

def loadLat():
    latData = []
    fh = open("US Cities Lat.csv")
    data = fh.readlines()
    small_arr = []
    for item in data:
        small_arr = item.split(',')
        small_arr[1] = small_arr[1].replace("\n", "")
        small_arr[1] = small_arr[1].replace("\r", "")
            
        latData.append(small_arr)
    return(latData)

#modify temp experienced for each group
#new mu values equal to functions of temp
def mortalityCalc(climDataExtreme, year):
    
#initialize variables (weight in g)
#since climate data is in F and the rest is in C, we must switch to C
    airTempF = 105
    airTempC = (airTempF-32.0)*(5.0/9.0)
    
#Baseline weight from https://www.ovocontrol.com/pigeon-facts-figures
    baselineWeight = 296.67
#pull in days over air temp from climate data
    days = 0
    for item in climDataExtreme:
        if item[0] == str(year):
            days = float(item[1])
    

#air temp to body temp using data source: Calder, W. A., & Schmidt-Nielsen, K. (1967). Temperature regulation and evaporation in the    pigeon and the roadrunner. American Journal of Physiology-Legacy Content, 213(4), 883-889. doi:10.1152/ajplegacy.1967.213.4.883
#0.5 is from paper: Angelier F. Pigeons in the sun: Thermal constraints of eumelanic plumage in the rock pigeon (Columba livia).        Journal of Thermal Biology. 2020 May;90:102601. DOI: 10.1016/j.jtherbio.2020.102601. PMID: 32479396.
    bodyTemp1 = 34.2297 + (airTempC)*0.1789 +0.5
    bodyTemp2 = 34.2297 + (airTempC)*0.1789 +0.5
    bodyTemp3 = 34.2297 + (airTempC)*0.1789
    
#body temp to EWL using data source: Calder, W. A., & Schmidt-Nielsen, K. (1967). Temperature regulation and evaporation in the    pigeon and the roadrunner. American Journal of Physiology-Legacy Content, 213(4), 883-889. doi:10.1152/ajplegacy.1967.213.4.883
    EWL1 = -417.19 + (bodyTemp1)*10.45 
    EWL2 = -417.19 + (bodyTemp2)*10.45
    EWL3 = -417.19 + (bodyTemp3)*10.45

#calculate the proportion of the weight lost through EWL
#baseline pigeon weight = 297.67 (average weight from ovocontrol website)
    prop1 = (baselineWeight-EWL1)/baselineWeight
    prop2 = (baselineWeight-EWL2)/baselineWeight
    prop3 = (baselineWeight-EWL3)/baselineWeight

#mortality calculation based on proportion of weight lost using data source: #data source: B.W. Bierer, T.H. Eleazer, B.D. Barnett,     The Effect of Feed and Water Deprivation on Water and Feed Consumption, Body Weight and Mortality in Broiler Chickens of Various        Ages, Poultry Science, Volume 45, Issue 5, 1966, Pages 1045-1051, ISSN 0032-5791, https://doi.org/10.3382/ps.0451045                    (https://www.sciencedirect.com/science/article/pii/S0032579119380721)
#find correspoding point on mortality curve = per day mortality
#mortality rates (mu = (1-x)^days)
#x = mortality
    x1 = 1.0-0.0006319*(e**(22.08*(prop1)**2.0))
    x2 = 1.0-0.0006319*(e**(22.08*(prop2)**2.0))
    x3 = 1.0-0.0006319*(e**(22.08*(prop3)**2.0))

    
#surivival prob per year
    mu1 = (1.0-x1)**days
    mu2 = (1.0-x2)**days
    mu3 = (1.0-x3)**days

    return mu1, mu2, mu3