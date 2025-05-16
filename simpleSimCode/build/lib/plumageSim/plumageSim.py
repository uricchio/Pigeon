import sys
import os
import numpy as np
import re
import math
import mpmath
import llist
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve
from scipy.special import gammaincc
from scipy.special import gamma
from scipy.special import owens_t
from scipy.special import erf
from collections import defaultdict
from scipy.stats import skewnorm

class SimulatePlumage():

    def __init__(self,N=1000000,s_a=-0.00001,s_A=-0.01,p=0.5,S=0.0005,x_T=48, dx_T=0.5, d=0.01,
                  tempFile="/Users/uricchio/projects/Pigeon/tempData/Phoenix.GHCND:USW00023183.tMax.csv",
                  year =1940,flip=False):
        self.N = N
        self.s_A = s_A
        self.p = p
        self.S = S
        self.d = d
        self.dx_T = dx_T
        self.x_T = x_T
        self.t = 0
        self.d_a = 0
        self.d_A = 0
        self.paramsSkewNorm = {}
        self.year = year
        self.year0 = year
        self.flip = flip
        self.tempFile = tempFile
        self.daysAbove = {}
        self.getSkewNormal()
        self.getDays()
        self.s_a = self.get_sa(p)

    def dDelQ(self):
        num =- 2*(self.s_a+self.s_A)**2 * (self.qEq()**3) * (self.qEq()-1)
        den = self.s_A*(1-self.S)**self.d_a + self.s_a*(self.s_A+(1-self.S)**self.d_A)
        return num/den

    # function to do W-F model given current population status
    def nextGen(self):
        
        self.getDays()       
   
        # get fitnesses of phenotypes
        Waa = self.s_a*self.p + (1-self.S)**self.d_a
        WA = self.s_A*(1-self.p) + (1-self.S)**self.d_A

        # get expected frequencies in next generation and sample from binomial
        fExp = (self.p*Waa + (self.p**0.5)*(1-self.p**0.5)*WA)/(self.p*Waa + (1-self.p)*WA)

        if fExp < 0:
            fExp = 0. 
        elif fExp > 1:
            fExp = 1. 

        f = np.random.binomial(2*self.N, fExp)/(self.N*2)
        self.p = f**2

        print(self.p,fExp**2,self.qEq(),self.p*(self.x_T-self.dx_T)+(1-self.p)*(self.x_T),((1-self.S)**self.d_A-(1-self.S)**self.d_a),self.S*(self.d_a-self.d_A),self.x_T,self.year-1939,self.s_a,self.dDelQ())

        self.year += 1
        return

    # function to select new d_A and d_a
    def getDays(self):
 
        offset = self.d*(self.year-self.year0)
        if self.year > 2100:
            offset = self.d*(2100-self.year0)

        year = self.year0
        self.d_A = 183*(1-skewnorm.cdf(self.x_T,a=self.paramsSkewNorm[year][0],loc=offset+self.paramsSkewNorm[year][1],scale=self.paramsSkewNorm[year][2]))
        self.d_a = 183*(1-skewnorm.cdf(self.x_T-self.dx_T,a=self.paramsSkewNorm[year][0],loc=offset+self.paramsSkewNorm[year][1],scale=self.paramsSkewNorm[year][2]))   
        if self.flip:
            self.d_a = 183*(1-skewnorm.cdf(self.x_T,a=self.paramsSkewNorm[year][0],loc=offset+self.paramsSkewNorm[year][1],scale=self.paramsSkewNorm[year][2]))
            self.d_A = 183*(1-skewnorm.cdf(self.x_T-self.dx_T,a=self.paramsSkewNorm[year][0],loc=offset+self.paramsSkewNorm[year][1],scale=self.paramsSkewNorm[year][2]))   

    def qEq(self):
        return ((self.s_A + (-(1-self.S)**self.d_a+(1-self.S)**self.d_A))/(self.s_A+self.s_a))

    def get_sa(self,q):
        return ((1-q)*self.s_A+(1-self.S)**self.d_A-(1-self.S)**self.d_a)/q
 
    def getSkewNormal(self,prParams=False):
        fh=open(self.tempFile,'r')

        # skip first line
        for line in fh:
            break

        temps = {}

        # get temp data
        for line in fh:
            line = line.strip()
            line=line.replace("\",\"","*")
            data=line.split("*")

            if len(data) < 4:
                 continue

            # don't include winter months
            month = int(data[2][5:7])
            if month < 4 or month > 9:
                continue

            year = int(data[2][0:4])
            temp = (float(data[3][:-1])-32)*5/9

            if year not in temps:
                temps[year] = []
            temps[year].append(temp)

        for year in temps:
            params = skewnorm.fit(temps[year]) #,floc=np.mean(temps[year])))  
            self.paramsSkewNorm[int(year)] = [params[0], params[1], params[2]]
             
            if prParams and year != 1945:
                print(year, params[0], params[1], params[2], params[1] + params[2]*((2/np.pi)**0.5) *params[0]/(1+params[0]**2)**0.5, np.mean(temps[year]))


    def getdA_minus_da(self):

        fh=open(self.tempFile,'r')

        # skip first line
        for line in fh:
            break

        temps = {}

        # get temp data
        for line in fh:
            line = line.strip()
            line=line.replace("\",\"","*")
            data=line.split("*")

            if len(data) < 4:
                 continue

            # don't include winter months
            month = int(data[2][5:7])
            if month < 4 or month > 9:
                continue

            year = int(data[2][0:4])
            temp = (float(data[3][:-1])-32)*5/9

            if year not in temps:
                temps[year] = []
            temps[year].append(temp)

        # for each year, get the number of days above x_T and x_T-dx_T and expected number of days above x_T and dx_T
        for year in temps:
            if year != 1945:
                exp_above_0 = skewnorm.cdf(self.x_T,a=self.paramsSkewNorm[year][0],loc=self.paramsSkewNorm[year][1],scale=self.paramsSkewNorm[year][2])
                exp_above_1 = skewnorm.cdf(self.x_T-self.dx_T,a=self.paramsSkewNorm[year][0],loc=self.paramsSkewNorm[year][1],scale=self.paramsSkewNorm[year][2])
                emp_above_0 = 0
                emp_above_1 = 0

                for temp in temps[year]:
                    if temp > self.x_T:
                        emp_above_0 += 1
                    if temp > self.x_T-self.dx_T:
                        emp_above_1 += 1

                emp_above_0 /= len(temps[year])    
                emp_above_1 /= len(temps[year])    

                print(year,self.x_T,self.dx_T, 1-exp_above_0,emp_above_0,1-exp_above_1,emp_above_1)
