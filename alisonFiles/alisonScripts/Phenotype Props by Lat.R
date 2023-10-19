#data source: Obukhova, N.Y. Dynamics of balanced polymorphism morphs in blue rock pigeon Columbia livia . Russ J Genet 47, 83–89 (2011). https://doi.org/10.1134/S1022795411010078

plot(Latitude, Proportion, col = colorID, xlab = "Latitude (Nº)", ylab = "Phenotype Proportion",main = "Phenotype Frequecy vs. Latitude", xlim = c(40,60), ylim = c(0,0.70))
legend("top" ,pch=1, legend=c("Blue", "Melanistic", "Intermediate", "Aberrant"),col=c("red", "blue", "green", "black"))
abline(lm(PigeonBlue$Proportion ~ PigeonBlue$`Latitude (°N)`), col = "red")
abline(lm(PigeonMelan$Proportion ~ PigeonMelan$`Latitude (°N)`), col = "blue")
abline(lm(PigeonInt$Proportion ~ PigeonInt$`Latitude (°N)`), col = "green")
abline(lm(PigeonAberrant$Proportion ~ PigeonAberrant$`Latitude (°N)`), col = "black")
BlueCoeff<-lm(PigeonBlue$Proportion ~ PigeonBlue$`Latitude (°N)`)
MelanCoeff<-lm(PigeonMelan$Proportion ~ PigeonMelan$`Latitude (°N)`)
IntCoeff<-lm(PigeonInt$Proportion ~ PigeonInt$`Latitude (°N)`)
AberrantCoeff<-lm(PigeonAberrant$Proportion ~ PigeonAberrant$`Latitude (°N)`)



