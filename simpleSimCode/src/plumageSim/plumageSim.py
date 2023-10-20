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
from collections import defaultdict

class SimulatePlumage():

    def __init__(self,N=5000,s_a=-0.1,s_A=-0.1,p=0.01,S=0.01,alpha=1,beta=1):
        self.N = N
        self.s_A = s_A
        self.s_a = s_a
        self.p = p
        self.S = S
        self.alpha = alpha
        self.beta = beta
        # get self.d_a and self.d_A
        self.d_a = 12
        self.d_A = 10

    # function to do W-F model given current population status
    def nextGen(self):
          
        # get fitnesses of phenotypes
        Waa = self.s_a*self.p + (1-self.S)**self.d_a
        WA = self.s_A*(1-self.p) + (1-self.S)**self.d_A

        # get expected frequencies in next generation and sample from binomial
        fExp = (self.p*Waa + (self.p**0.5)*(1-self.p**0.5)*WA)/(self.p*Waa + (1-self.p)*WA)

        f = np.random.binomial(2*self.N, fExp)/(self.N*2)
        self.p = f**2

        print(self.p)

        return
  
    def TotalDgTmax(self, a,b,d,t,x_T):

        const= a + b*d*t
        num = (x_T**(const**2 / a)) * ((b*const/a)**(const**2 / a)) * ((x_T * b * const/a)**(-(const**2)/a))
        num *= (-special.gamma(const**2 / a) + special.gamma(const**2 / a)*special.gammaincc(const**2 / a, x_T*b*const/a))

        denom = special.gamma(const**2/a)

        return (1 + num/denom)

    def diff_da_dA(self,a,b,d,t,x_T,dx_T):
        
        return 365*(self.TotalDgTmax(a,b,d,t,x_T-dx_T) - self.TotalDgTmax(a,b,d,t,x_T))

    # function to select new d_A and d_a
    def getDays(self,a,b,d,t,x_T,d_xT):
 
        
