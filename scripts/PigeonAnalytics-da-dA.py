from scipy import special
import numpy as np

def TotalDgTmax(a,b,d,t,x_T):
   
    const= a + b*d*t
    num = (x_T**(const**2 / a)) * ((b*const/a)**(const**2 / a)) * ((x_T * b * const/a)**(-(const**2)/a)) 
    num *= (-special.gamma(const**2 / a) + special.gamma(const**2 / a)*special.gammaincc(const**2 / a, x_T*b*const/a))

    denom = special.gamma(const**2/a)
   
    return (1 + num/denom)

def diff_da_dA(a,b,d,t,x_T,dx_T):
    return 365*(TotalDgTmax(a,b,d,t,x_T-dx_T) - TotalDgTmax(a,b,d,t,x_T))

a = 26.4
b = 0.31
d = 0.32
x_T = 90

for t in np.arange(0,100):
    for x_T in [80,100,120]:
        for dx_T in [0.1,0.2,0.5,1,2]:
            for S_sa in [0.1,0.2,0.5,1]:                
                print(t,x_T,dx_T,S_sa,S_sa*diff_da_dA(a,b,d,t,x_T,dx_T))

    
