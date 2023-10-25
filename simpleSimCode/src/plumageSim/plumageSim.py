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

    def __init__(self,N=5000,s_a=-0.01,s_A=-0.02,p=0.5,S=0.01,alpha=26.4,beta=0.31,x_T=80,dx_T=0.5):
        self.N = N
        self.s_A = s_A
        self.s_a = s_a
        self.p = p
        self.S = S
        self.a = alpha
        self.b = beta
        self.d = 0.32
        self.dx_T = dx_T
        self.x_T = x_T
        self.t = 0
        self.d_a = 0
        self.d_A = 0
        self.getDays()

    # function to do W-F model given current population status
    def nextGen(self):
      
        self.getDays()       
   
        # get fitnesses of phenotypes
        Waa = self.s_a*self.p + (1-self.S)**self.d_a
        WA = self.s_A*(1-self.p) + (1-self.S)**self.d_A

        # get expected frequencies in next generation and sample from binomial
        fExp = (self.p*Waa + (self.p**0.5)*(1-self.p**0.5)*WA)/(self.p*Waa + (1-self.p)*WA)

        f = np.random.binomial(2*self.N, fExp)/(self.N*2)
        self.p = f**2

        self.t += 1

        print(self.p,-1.*self.S*(self.da-self.dA)/self.s_a)

        return
  
    def TotalDgTmax(self,x_T):

        a = self.a
        b = self.b
        d = self.d
        t = self.t

        const= a + b*d*t
        num = (x_T**(const**2 / a)) * ((b*const/a)**(const**2 / a)) * ((x_T * b * const/a)**(-(const**2)/a))
        num *= (-gamma(const**2 / a) + gamma(const**2 / a)*gammaincc(const**2 / a, x_T*b*const/a))

        denom = gamma(const**2/a)

        return (1 + np.exp(num/denom))

    # function to select new d_A and d_a
    def getDays(self):
 
        self.dA = 365*self.TotalDgTmax(self.x_T)
        self.da = 365*self.TotalDgTmax(self.x_T-self.dx_T)

        return

   
