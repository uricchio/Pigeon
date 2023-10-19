#data source: Obukhova, N.Y. Dynamics of balanced polymorphism morphs in blue rock pigeon Columbia livia . Russ J Genet 47, 83–89 (2011). https://doi.org/10.1134/S1022795411010078

plot(Latitude, Phenotype.frequency, col = colorID, xlab = "Latitude (Nº)", ylab = "Phenotype Frequency (%)",main = "Phenotype Frequecy vs. Latitude", xlim = c(40,60), ylim = c(0,70))
legend("top" ,pch=1, legend=c("Blue", "Melanistic", "Intermediate", "Aberrant"),col=c("red", "blue", "green", "black"))
abline(lm(PigeonBlue$`%` ~ PigeonBlue$`Latitude (°N)`), col = "red")
abline(lm(PigeonMelan$`%` ~ PigeonMelan$`Latitude (°N)`), col = "blue")
abline(lm(PigeonInt$`%` ~ PigeonInt$`Latitude (°N)`), col = "green")
abline(lm(PigeonAberrant$`%` ~ PigeonAberrant$`Latitude (°N)`), col = "black")
BlueCoeff<-lm(PigeonBlue$`%` ~ PigeonBlue$`Latitude (°N)`)
MelanCoeff<-lm(PigeonMelan$`%` ~ PigeonMelan$`Latitude (°N)`)
IntCoeff<-lm(PigeonInt$`%` ~ PigeonInt$`Latitude (°N)`)
AberrantCoeff<-lm(PigeonAberrant$`%` ~ PigeonAberrant$`Latitude (°N)`)
coefficientsData<-data.frame()
coefficientsData<-rbind(coefficientsData, data.frame(Intercept = BlueCoeff$coefficients[1], Latitude = BlueCoeff$coefficients[2], color = "Blue"))
coefficientsData<-rbind(coefficientsData, data.frame(Intercept = MelanCoeff$coefficients[1], Latitude = MelanCoeff$coefficients[2], color = "Melanistic"))
coefficientsData<-rbind(coefficientsData, data.frame(Intercept = IntCoeff$coefficients[1], Latitude = IntCoeff$coefficients[2], color = "Intermediate"))
coefficientsData<-rbind(coefficientsData, data.frame(Intercept = AberrantCoeff$coefficients[1], Latitude = AberrantCoeff$coefficients[2], color = "Aberrant"))
write.table(coefficientsData, file = "~/PigeonFile")




