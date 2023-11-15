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

    def __init__(self,N=1000000,s_a=-0.0002,s_A=-0.001,p=0.5,S=0.001,x_T=38,dx_T=0.5, d=0.05,
                  tempFile="/Users/uricchio/projects/Pigeon/tempData/Phoenix.GHCND:USW00023183.tMax.csv",
                  year =1940):
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
        self.tempFile = tempFile
        self.daysAbove = {}
        self.getSkewNormal()
        self.getDays()
        self.s_a = self.get_sa(p)

    # function to do W-F model given current population status
    def nextGen(self):
        
        self.getDays()       
   
        # get fitnesses of phenotypes
        Waa = self.s_a*self.p + (1-self.S)**self.d_a
        WA = self.s_A*(1-self.p) + (1-self.S)**self.d_A

        # get expected frequencies in next generation and sample from binomial
        fExp = (self.p*Waa + (self.p**0.5)*(1-self.p**0.5)*WA)/(self.p*Waa + (1-self.p)*WA)

        if fExp < 0:
            fExp = 0. # 1./(self.N*2)
        elif fExp > 1:
            fExp = 1. #1-1./(self.N*2)

        f = np.random.binomial(2*self.N, fExp)/(self.N*2)
        self.p = f**2

        print(self.p,fExp**2,self.qEq(),self.p*(self.x_T-self.dx_T)+(1-self.p)*(self.x_T),((1-self.S)**self.d_a-(1-self.S)**self.d_A),self.S*(self.d_A-self.d_a),self.x_T,self.year-1939)

        self.year += 1
        return

    # skewnorm model   
    def TotalDgTmax(self,x_T,useYears =False):
        
        scale = 0
        loc = 0
        alpha = 0
        if useYears:
            year = self.year
            if self.year < 2022:
                while year not in self.paramsSkewNorm:
                    year-=1    
            else:
                year = 2022
            scale = self.paramsSkewNorm[year][2]
            alpha = self.paramsSkewNorm[year][0]
            loc = self.paramsSkewNorm[year][1] 

        else:
           if self.year < 2100: 
               scale = self.paramsSkewNorm[self.year0][2]
               alpha = self.paramsSkewNorm[self.year0][0]
               loc = self.paramsSkewNorm[self.year0][1]+self.d*(self.year-self.year0)
           else: 
               scale = self.paramsSkewNorm[self.year0][2]
               alpha = self.paramsSkewNorm[self.year0][0]
               loc = self.paramsSkewNorm[self.year0][1]+self.d*(2100-self.year0)

        t1 = 0.5*(1+erf(((x_T-loc)/scale)/(2**0.5)))
        t2 = owens_t((x_T-loc)/scale,alpha)

        return t1 - 2*t2
    
    # function to select new d_A and d_a
    def getDays(self):
 
        self.d_A = 183*self.TotalDgTmax(self.x_T)
        self.d_a = 183*self.TotalDgTmax(self.x_T-self.dx_T)

    def qEq(self):
        return (self.s_A - ((1-self.S)**self.d_a-(1-self.S)**self.d_A))/(self.s_A+self.s_a)

    def get_sa(self,q):
        return ((1-q)*self.s_A-(1-self.S)**self.d_a+(1-self.S)**self.d_A)/q
 
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
