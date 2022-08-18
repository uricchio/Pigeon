#data source: B.W. Bierer, T.H. Eleazer, B.D. Barnett, The Effect of Feed and Water Deprivation on Water and Feed Consumption, Body Weight and Mortality in Broiler Chickens of Various Ages, 
  #Poultry Science, Volume 45, Issue 5, 1966, Pages 1045-1051, ISSN 0032-5791, https://doi.org/10.3382/ps.0451045. 
  #(https://www.sciencedirect.com/science/article/pii/S0032579119380721)

weight<-c(125,118,114,110,105,102,98,94,91,88,85,82,79,76,71,69,66,62,62,61,60,58,56,55,55,54,54)/125
surv<-c(1,1,1,1,1,1,1,1,1,7/8,7/8,7/8,7/8,7/8,7/8,7/8,7/8,7/8,7/8,7/8,6/8,5/8,4/8,3/8,3/8,2/8,1/8) 

plot(1-weight,surv,pch=20,xlab="Proportion of Weight Lost",ylab="Proportion Surviving")

#fit a model
model<-nls(surv ~ 1-a*exp(-lam*(1-weight)^2), start = list(a = 0.5, lam = -0.2))
nls_coef<-coef(model)
lines(1-weight, 1-nls_coef[1]*exp(-nls_coef[2]*(1-weight)^2), col = "orange2", lwd = 2)


# calc for weight at which 95% survive
-log(0.05/(nls_coef[1]))/nls_coef[2] + 1

# calc for 
1-nls_coef[1]*exp(nls_coef[2]*(1-0.5434))
