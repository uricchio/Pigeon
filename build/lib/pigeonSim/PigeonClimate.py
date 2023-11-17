import sys
import os
import numpy as np
import re
import math
import mpmath
import llist
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve
from collections import defaultdict

class SimulatePigeon():

    def __init__(self,N=1000,phi=0.1,s_a=0.1,s_j=0.1,N_males=0,p=0.2,q=0.3,mort=0.3,s_b=0.1,s_A=0.2,P0=0.9,PK=0.42,K=5000,B=2,ncz=0.5,repOut=3,juvMort = 0.5):
        self.N = N
        self.phi = phi
        self.mort = mort
        self.s_b = s_b
        self.s_A = s_A
        self.K = K
        self.PK = PK
        self.P0 = P0
        self.B=2
        self.ncz = ncz
        self.repOut = repOut
        self.juvMort = juvMort
        if N_males == 0:
            N_males = np.random.poisson(N/2)
        N_females  = N-N_males
         
        # now make age/sex/pheno dist        
        pop = {}
        
        # find number of males in each pheno class
        N_male_vec = np.random.multinomial(N_males, [p**2,2*p*q,q**2,(1-p-q)*q*2,(1-p-q)**2,(1-p-q)*p*2],size=1)

        pop[("M",0,"bb")] = N_male_vec[0][0]
        pop[("M",0,"bB")] = N_male_vec[0][1]
        pop[("M",0,"BB")] = N_male_vec[0][2]
        pop[("M",0,"BA")] = N_male_vec[0][3]
        pop[("M",0,"AA")] = N_male_vec[0][4]
        pop[("M",0,"bA")] = N_male_vec[0][5]
  
        N_female_vec = np.random.multinomial(N_females, [p, q, 1-(p+q)],size=1)
        
        pop[("F",0,"b")] = N_female_vec[0][0]
        pop[("F",0,"B")] = N_female_vec[0][1]
        pop[("F",0,"A")] = N_female_vec[0][2]
 
        self.pop = pop
     
        # now make arrays of individuals with Geno, Sex, Age, and exposure
        self.indsM = llist.sllist()
        self.indsF = llist.sllist()
        for ageSexGenoClass in self.pop:
            for i in range(self.pop[ageSexGenoClass]):
                if ageSexGenoClass[0] == "M":
                    self.indsM.appendnode(llist.sllistnode([ageSexGenoClass[1],ageSexGenoClass[2],0]))  
                else:    
                    self.indsF.appendnode(llist.sllistnode([ageSexGenoClass[1],ageSexGenoClass[2],0]))  


    def genOffspring(self,mother,father):
        # get expected rep output
        repOut = self.repOut
        if mother[2] == 1:
            repOut=self.ncz*self.repOut

        # sample number of offspring
        offs = np.random.poisson(repOut)
       
        # get offspring genos
        genos = []
        for i in range(offs):  
   
            father_g = father[1][1]
            if np.random.random() > 0.5:
                father_g = father[1][0]
            mother_g = ""
            if np.random.random() > 0.5:
                mother_g = mother[1] 
            geno = father_g+mother_g
            if mother_g > father_g:
                 geno = mother_g+father_g
            genos.append(geno)
        return genos

    def pheno(self,geno):
        if geno == "A":
            return 1+self.s_A
        elif geno == "B":
            return 1
        elif geno == "b":
            return 1+self.s_b
        elif geno == "BB":
            return 1
        elif geno == "BA":
            return 1+self.s_A
        elif geno == "bA":
            return 1+self.s_A
        elif geno == "AA":
           return  1+self.s_A
        elif geno == "bB":
           return 1
        elif geno == "bb":
           return 1+self.s_b

    def probExp(self,age):
        # probability of ncz exposure, which depends on age
        return 1 

    def densDep(self, N):
        # Giunchi et al 2007 density dependence
        return self.P0 - ((self.P0-self.PK)*(N/self.K)**self.B)

    def phenoTemp(self,geno,days):
        # not actually a good model!
        if geno == "A":
            return (1-self.s_A)**days
        elif geno == "B":
            return 1
        elif geno == "b":
            return 1+self.s_b
        elif geno == "BB":
            return 1
        elif geno == "BA":
            return (1-self.s_A)**days
        elif geno == "bA":
            return (1-self.s_A)**days
        elif geno == "AA":
           return  (1-self.s_A)**days
        elif geno == "bB":
           return 1
        elif geno == "bb":
           return (1-self.s_b)**days
 
    def nextGen(self):
        # first mortality, which is phenotype dependent
        i = 0
        while i < self.indsM.size:
            if np.random.random() < self.mort*self.pheno(self.indsM.nodeat(i).value[1]):
               self.indsM.remove(self.indsM.nodeat(i))
               continue      
            i += 1
        
        i = 0
        while i < self.indsF.size:
            if np.random.random() < self.mort*self.pheno(self.indsF.nodeat(i).value[1]):
               self.indsF.remove(self.indsF.nodeat(i))
               continue      
            i += 1

        # next all remaining inds age a year
        for i in range(len(self.indsM)):
            self.indsM[i][0] += 1
        for i in range(len(self.indsF)):
            self.indsF[i][0] += 1
 
        # next get drug exposure, more likely for older individuals
        for node in self.indsM.iternodes():
            if np.random.random() < self.probExp(node.value[0]):
                node.value[2] = 1

        # now reproduce -- Giunchi et al 2007 density dependence
        numRepPairs = np.random.binomial(self.indsF.size,self.densDep(self.indsM.size+self.indsF.size))             
        
        # randomly select numRepPairs from amongst females
        femaleNodes = np.random.choice(self.indsF.size,numRepPairs,replace=False)        

        # randomly select numRepPairs from amongst males
        maleNodes = np.random.choice(self.indsM.size,numRepPairs)        

        juves = []
        # generate offspring for each pair   
        for i in range(numRepPairs):
            offs = self.genOffspring(self.indsF[femaleNodes[i]],self.indsM[maleNodes[i]])
            juves.append(offs)
         
        # lastly, selection on temp for juveniles 
        # selection depends on fitness cost, which depends on number of days above T thresh
        # add this feature later
        for i in range(numRepPairs):	
            for j in range(len(juves[i])):
                # if surv, add to pop
                if np.random.random() > self.juvMort*self.phenoTemp(juves[i][j],1.7):
                    if len(juves[i][j]) == 1:
                        self.indsF.appendnode(llist.sllistnode([0,juves[i][j],0]))
                    else:
                        self.indsM.appendnode(llist.sllistnode([0,juves[i][j],0]))       
      
        pM = 0
        for ind in self.indsM:
            pM += ind[1].count("B")
        pM /= (2*self.indsM.size)

        pF = 0
        for ind in self.indsF:
            pF += ind[1].count("B")
        pF /= self.indsF.size

        print((2*pM+pF)/3)

        # make pop values for each geno
        return

