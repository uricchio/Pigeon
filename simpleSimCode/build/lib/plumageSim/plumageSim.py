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
from collections import defaultdict

class SimulatePlumage():

    def __init__(self,N=10000,s_a=-0.01,s_A=-0.001,p=0.8,S=0.0001,alpha=12.09,beta=0.39,x_T=38,dx_T=1):
        self.N = N
        self.s_A = s_A
        self.p = p
        self.S = S
        self.a = alpha
        self.b = beta
        self.d = 0.1
        self.dx_T = dx_T
        self.x_T = x_T
        self.t = 0
        self.d_a = 0
        self.d_A = 0
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

        print(self.p,fExp**2,self.qEq(),self.p*(self.x_T-self.dx_T)+(1-self.p)*(self.x_T))

        self.t += 1
        return

    # gamma model   
    def TotalDgTmax(self,x_T):

        a = self.a
        b = self.b
        d = self.d
        t = self.t
        if t > 100:
            t = 100

        const= a + b*d*t
        num = (x_T**(const**2 / a)) * ((b*const/a)**(const**2 / a)) * ((x_T * b * const/a)**(-(const**2)/a))
        num *= (-gamma(const**2 / a) + gamma(const**2 / a)*gammaincc(const**2 / a, x_T*b*const/a))

        denom = gamma(const**2/a)

        return (1 + num/denom)

    # linear model
    def TotalDgTmaxLin(self,x_T0,m):
        
        t = self.t
        if t > 100:
             t = 100
        return m*t + x_T0

    # function to select new d_A and d_a
    def getDays(self):
 
        self.d_A = 365*self.TotalDgTmax(self.x_T)
        self.d_a = 365*self.TotalDgTmax(self.x_T-self.dx_T)

        return

    def qEq(self):
        return (self.s_A - ((1-self.S)**self.d_a-(1-self.S)**self.d_A))/(self.s_A+self.s_a)

    def get_sa(self,q):
        return ((1-q)*self.s_A-(1-self.S)**self.d_a+(1-self.S)**self.d_A)/q
        

