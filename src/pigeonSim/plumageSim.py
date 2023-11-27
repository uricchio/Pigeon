import sys
import os
import numpy as np
from scipy.stats import skewnorm

class SimulatePigeon():

    # blue is most common, so s_b should have weakest frequency-dependent penalty

    def __init__(self,N=100000,s_A=-0.005,s_b=-0.0002,s_B=-0.0001,p=0.1,q=0.3,S=0.001,x_T=43,dx_T_B=0.5,dx_T_b=1,d=0.1,
                  tempFile="/Users/uricchio/projects/Pigeon/tempData/Phoenix.GHCND:USW00023183.tMax.csv",
                  year =0):
        self.N = N
        self.s_A = s_A
        self.s_b = s_b
        self.s_B = s_B
        self.p = p
        self.q = q
        self.S = S
        self.d = d
        self.dx_T_B = dx_T_B
        self.dx_T_b = dx_T_b
        self.x_T = x_T
        self.t = 0
        self.d_A = 0
        self.d_b = 0
        self.d_B = 0
        self.paramsSkewNorm = {}
        self.year = year
        self.year0 = year
        self.tempFile = tempFile
        self.getSkewNormal()
        self.getDays()

    # function to do W-F model given current population status
    def nextGen(self):
        
        self.getDays()       
  
        A_Pheno_male = self.p**2 + 2*self.p*self.q + 2*self.p*(1-(self.p+self.q)) 
        B_Pheno_male = 2*(1-self.p-self.q)*self.q + self.q**2
        b_Pheno_male = (1-(self.p+self.q))**2 

        A_Pheno_female = self.p
        B_Pheno_female = self.q
        b_Pheno_female = 1-(self.p+self.q)

        # get fitnesses of phenotypes
        WA_male = self.s_A*(A_Pheno_male) + (1-self.S)**self.d_A
        WB_male = self.s_B*(B_Pheno_male) + (1-self.S)**self.d_B
        Wb_male = self.s_b*(b_Pheno_male) + (1-self.S)**self.d_b

        WA_female = self.s_A*(A_Pheno_female) + (1-self.S)**self.d_A
        WB_female = self.s_B*(B_Pheno_female) + (1-self.S)**self.d_B
        Wb_female = self.s_b*(b_Pheno_female) + (1-self.S)**self.d_b

        # get male freqs        
        f_AA_exp = WA_male*(self.p**2 + self.p*self.q + self.p*(1-(self.p+self.q)))*WA_female*self.p
        f_AB_exp = WA_male*(self.p**2 + self.p*self.q + self.p*(1-(self.p+self.q)))*WB_female*self.q+WA_male*(self.p*self.q)*WA_female*self.p+ WB_male*((1-self.p-self.q)*self.q + self.q**2)*WA_female*self.p
        f_Ab_exp = WA_male*(self.p**2 + self.p*self.q + self.p*(1-(self.p+self.q)))*Wb_female*(1-(self.p+self.q))+ Wb_male*((1-(self.p+self.q))**2)*WA_female*self.p +WB_male*(self.q*(1-self.p*self.q))*WA_female*self.p

        f_BB_exp = WA_male*(self.p*self.q)*WB_female*self.q + WB_male*((1-self.p-self.q)*self.q + self.q**2)*WB_female*self.q
        f_Bb_exp = WA_male*(self.p*self.q)*Wb_female*(1-self.q-self.p) + WA_male*(self.p*(1-(self.p+self.q)))*WB_female*self.q + WB_male*((1-self.p-self.q)*self.q + self.q**2)*Wb_female*(1-self.p-self.q)+Wb_male*((1-(self.p+self.q))**2)*WB_female*self.q
       
        f_bb_exp = WA_male*(self.p*(1-(self.p+self.q)))*Wb_female*(1-(self.q+self.p))+  WB_male*((1-self.p-self.q)*self.q)*Wb_female*(1-(self.q+self.p)) + Wb_male*((1-(self.p+self.q))**2)*Wb_female*(1-(self.q+self.p))

        totFit = f_AA_exp + f_AB_exp + f_Ab_exp + f_BB_exp + f_Bb_exp + f_bb_exp
        f_AA_exp/= totFit
        f_AB_exp/= totFit
        f_Ab_exp/= totFit
        f_BB_exp/= totFit
        f_Bb_exp/= totFit
        f_bb_exp/= totFit

        # get female freqs
        f_A_exp = WA_female*self.p  
        f_B_exp = WB_female*self.q
        f_b_exp = Wb_female*(1-self.p-self.q)

        totFit = f_A_exp+f_B_exp+f_b_exp
        f_A_exp /= totFit 
        f_B_exp /= totFit 
        f_b_exp /= totFit 

        # get new frequencies with multinomial sampling
        
        new_male_counts = np.random.multinomial(self.N/2, [f_AA_exp,f_AB_exp,f_Ab_exp,f_BB_exp,f_Bb_exp,f_bb_exp])
        new_female_counts = np.random.multinomial(self.N/2, [f_A_exp,f_B_exp,f_b_exp])

        # get allele frequencies from genotype frequencies

        self.p = 2*(2*new_male_counts[0]+new_male_counts[1]+new_male_counts[2]+new_female_counts[0])/(3*self.N)
        self.q = 2*(2*new_male_counts[3]+new_male_counts[4]+new_male_counts[1]+new_female_counts[1])/(3*self.N)
            

        print(self.p, self.q, 1-self.p-self.q,self.d_A,self.d_B,self.d_b)
  
        self.year += 1
        return

    def getDays(self):

        offset = 0
        if self.year >= 1940 and self.year <= 2075:
            offset = self.d*(self.year-1940)
        if self.year > 2075:
            offset = self.d*(2075-1940)
        year = 1940
        self.d_A = 183*(1-skewnorm.cdf(self.x_T,a=self.paramsSkewNorm[year][0],loc=offset+self.paramsSkewNorm[year][1],scale=self.paramsSkewNorm[year][2]))
        self.d_B = 183*(1-skewnorm.cdf(self.x_T-self.dx_T_B,a=self.paramsSkewNorm[year][0],loc=offset+self.paramsSkewNorm[year][1],scale=self.paramsSkewNorm[year][2]))    
        self.d_b = 183*(1-skewnorm.cdf(self.x_T-self.dx_T_b,a=self.paramsSkewNorm[year][0],loc=offset+self.paramsSkewNorm[year][1],scale=self.paramsSkewNorm[year][2]))    

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

