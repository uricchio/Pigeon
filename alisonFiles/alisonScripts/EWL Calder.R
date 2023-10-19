#data source: Calder, W. A., & Schmidt-Nielsen, K. (1967). Temperature regulation and evaporation in the pigeon and the roadrunner. American Journal of Physiology-Legacy Content, 213(4), 883-889. doi:10.1152/ajplegacy.1967.213.4.883
#other publications used: Shannon R Conradie, Stephan M Woodborne, Blair O Wolf, Anaïs Pessato, Mylene M Mariette, Andrew E McKechnie, Avian mortality risk during heat waves will increase greatly in arid Australia during the 21st century, Conservation Physiology, Volume 8, Issue 1, 2020, coaa048, https://doi.org/10.1093/conphys/coaa048

plot(PigeonEWLData$`Air Temp (°C)`, PigeonEWLData$`Water evap. (g/5hr)`, xlab = "Air Temp (ºC)", ylab = "EWL (g/5hr)",main = "Evaporative Water Loss vs Air Temperature", xlim = c(30,60), ylim = c(0,45))
abline(lm(PigeonEWLData$`Water evap. (g/5hr)` ~ PigeonEWLData$`Air Temp (°C)` ), col = "blue")
abline(h=40.2, col="blue")
EWLAcoeff<-lm(PigeonEWLData$`Water evap. (g/5hr)` ~ PigeonEWLData$`Air Temp (°C)` )
EWLLineData<-data.frame()
EWLLineData<-rbind(EWLLineData, data.frame(Intercept = EWLcoeff$coefficients[1], Slope = EWLcoeff$coefficients[2]))
write.table(EWLLineData, file = "~/EWLFile")

plot(PigeonEWLData$`Body temp. (°C)`, PigeonEWLData$`Water evap. (g/5hr)`, xlab = "Body Temp (ºC)", ylab = "EWL (g/5hr)",main = "Evaporative Water Loss vs Body Temperature", xlim = c(35,50), ylim = c(0,50))
abline(lm(PigeonEWLData$`Water evap. (g/5hr)` ~ PigeonEWLData$`Body temp. (°C)` ), col = "blue")
abline(h=40.2, col="blue")
EWLBcoeff<-lm(PigeonEWLData$`Water evap. (g/5hr)` ~ PigeonEWLData$`Body temp. (°C)` )
EWLLineData<-data.frame()
EWLLineData<-rbind(EWLLineData, data.frame(Intercept = EWLcoeff$coefficients[1], Slope = EWLcoeff$coefficients[2]))
write.table(EWLLineData, file = "~/EWLFile")

plot(PigeonEWLData$`Air Temp (°C)` , PigeonEWLData$`Body temp. (°C)`, xlab = "Air Temp (ºC)", ylab = "Body Temp (ºC)",main = "Air Temperature vs Body Temperature", xlim = c(30,60), ylim = c(30,60))
abline(lm(PigeonEWLData$`Body temp. (°C)` ~ PigeonEWLData$`Air Temp (°C)` ), col = "blue")
EWLcoeff<-lm(PigeonEWLData$`Body temp. (°C)` ~ PigeonEWLData$`Air Temp (°C)` )
EWLLineData<-data.frame()
EWLLineData<-rbind(EWLLineData, data.frame(Intercept = EWLcoeff$coefficients[1], Slope = EWLcoeff$coefficients[2]))
write.table(EWLLineData, file = "~/EWLFile")