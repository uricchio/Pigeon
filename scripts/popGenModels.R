# 
library(ggplot2)
library(cowplot)
library(wesanderson)

read.table("~/projects/Pigeon/simData/sim.dx_T.2.d.0.02.txt")->popSims
  
lt = c()
for (thing in popSims$V3) {
  new = 1
  if (thing>1 || thing <0) {
    new <- new+1
  }
  lt <- c(lt,new)
}

popSims<-cbind(popSims,data.frame(lt=lt))

plA<-ggplot(data=popSims,aes(V8,V3,col=as.factor(V7),linetype=as.factor(lt)))+geom_line(size=0.7,alpha=0.5)+ylab(expression(italic(f[aa])))+scale_x_continuous(trans='log10',breaks=c(1,10,100,1000),labels=c(1940,1950,2040,2940))
plA<-plA+theme_classic()
plA<-plA+geom_point(aes(V8,V1),size=1.3)+ylim(c(0,1.2))+scale_color_manual(values=wes_palette("Zissou1",6,type="continuous"),name=expression(italic(X[T])),guide='none')
plA<-plA +xlab("year")+scale_linetype(guide="none")+theme(text = element_text(size=20))+theme(axis.line=element_line(size=1.4))

plB<-ggplot(data=popSims,aes(V8,V6,col=as.factor(V7)))+geom_line(size=0.7)+ylab(expression(italic(S(d[A]-d[a]))))+scale_x_continuous(trans='log10',breaks=c(1,10,100,1000),labels=c(1940,1950,2040,2940))
plB<-plB+theme_classic()
plB<-plB+scale_color_manual(values=wes_palette("Zissou1",6,type="continuous"),name=expression(italic(X[T])))+geom_line(aes(V8,V5),lty=2,alpha=0.7)
plB<-plB +xlab("year")+scale_linetype(guide="none")+theme(text = element_text(size=20))+theme(axis.line=element_line(size=1.4))
  
plot_grid(plA,plB,labels=c("A","B"),ncol=2,rel_widths = c(1,1.3))

ggsave("~/projects/Pigeon/Figures/popGenSims.pdf",height=3.2,width=11)

# pigeon sims

read.table("~/projects/Pigeon/simData/sim.Pigeon.d.0.02.Phoenix.txt")->p0p02
read.table("~/projects/Pigeon/simData/sim.Pigeon.d.0.1.Phoenix.txt")->p0p1

read.table("~/projects/Pigeon/simData/sim.Pigeon.d.0.02.Manhattan.txt")->m0p02
read.table("~/projects/Pigeon/simData/sim.Pigeon.d.0.1.Manhattan.txt")->m0p1

makePlot<- function(data) {
  plotDataFrame<-data.frame()
  i <- 1
  for (thing in data$V1) {
    if (i <= 1940) {
      i<-i+1
      next
    }
    
    plotDataFrame<-rbind(plotDataFrame,data.frame(t=i-1940,f=data$V1[i]^2/2 + data$V1[i]*data$V2[i]+data$V1[i]*data$V3[i]+data$V1[i]/2,geno="A"))
    plotDataFrame<-rbind(plotDataFrame,data.frame(t=i-1940,f=data$V2[i]^2/2 + data$V2[i]*data$V3[i]+data$V2[i]/2,geno="B"))
    plotDataFrame<-rbind(plotDataFrame,data.frame(t=i-1940,f=(data$V3[i]^2)/2+data$V3[i]/2,geno="b"))
    i <- i + 1
  }  
  
  
  
  return(plotDataFrame)
}

makePlot(p0p1) -> pigeon0p1
makePlot(p0p02) -> pigeon0p02

plA<-ggplot(pigeon0p02,aes(t,f,fill=geno))+geom_area()+scale_x_log10(breaks=c(1,10,100,1000),labels=c(1940,1950,2040,2940),name="year")+theme_classic()+scale_fill_manual(values=wes_palette("Royal1"),guide="none")+ylab(expression(italic(f * " (morph frequency)")))+theme(text = element_text(size=20))+theme(axis.line=element_line(size=1.4))
plB<-ggplot(pigeon0p1,aes(t,f,fill=geno))+geom_area()+scale_x_log10(breaks=c(1,10,100,1000),labels=c(1940,1950,2040,2940),name=expression("year"))+theme_classic()+scale_fill_manual(values=wes_palette("Royal1"),name="genotype")+ylab("")+theme(text = element_text(size=20))+theme(axis.line=element_line(size=1.4))

plot_grid(plA,plB,labels=c("A","B"),rel_widths = c(1,1.3))

ggsave("~/projects/Pigeon/Figures/Pigeon.Phoenix.pdf",width=12,height=3.6)


#make NY plots? They're boring

