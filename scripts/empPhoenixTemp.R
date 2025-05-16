library(ggplot2)
library(cowplot)
library(wesanderson)

# read Phoenix temp data
read.table("~/projects/Pigeon/tempData/Phoenix.TMax.params.txt")->params
scan("~/projects/Pigeon/tempData/Phoenix.tMax.1940.txt")->T1940

avg<-function(loc,scl,shp) {
  return(loc+scl*(shp/((1+shp**2)**0.5))*(2/pi)**0.5)
}

myStd<-function(scl,shp) {
  return ((scl**2 *(1-(2/pi)*(shp**2 / (1+shp**2))))**0.5) 
}

T1940<-data.frame(tM=T1940)
TDist<-data.frame(T=seq(24,50,0.5),dens=dsn(seq(24,50,0.5),xi=params$V3[6], omega=params$V4[6], alpha=params$V2[6]))
plA<-ggplot(data=T1940,aes(x=tM))+geom_histogram(binwidth=1,aes(y=..count../sum(..count..)),alpha=0.7)+geom_line(data=TDist,aes(T,dens),size=1)+theme_classic()
plA<-plA+theme(text = element_text(size=20))+theme(axis.line=element_line(size=1.4))+xlab(expression(italic(T[max])))+ylab("Density")


params<-cbind(params,data.frame(m=avg(params$V3,params$V4,params$V3),s=myStd(params$V4,params$V3)))

plB<-ggplot(params,aes(V1,m))+geom_smooth(method="lm",se=FALSE)+geom_point()+ylim(c(45,58))+theme_classic()+theme(text = element_text(size=20))+theme(axis.line=element_line(size=1.4))
plC<-ggplot(params,aes(V1,s))+geom_smooth(method="lm",se=FALSE)+geom_point()+theme_classic()+theme(text = element_text(size=20))+theme(axis.line=element_line(size=1.4))

plB<-plB+xlab("year")+ylab(expression(italic(E) *"[" * italic(T[max]) *"]"))
plC<-plC+xlab("year")+ylab(expression(italic(sigma) *"[" * italic(T[max]) *"]"))

plR<-plot_grid(plB,plC,ncol=1,labels=c("B","C"))

plot_grid(plA,plR,ncol=2,labels=c("A",""))

ggsave("~/projects/Pigeon/Figures/empPhoenixData.pdf",width=13,height=6)

# get params
summary(lm(params$m~params$V1))
summary(lm(params$s~params$V1))
# now the dA-da plot

read.table("~/projects/Pigeon/tempData/diff_dA_da.x_T.txt")->diffDays

pal <- wes_palette("Zissou1",6,type="continuous")
plA<-ggplot(data=diffDays,aes(V1,183*V4,col=as.factor(V2)))+geom_point()+geom_smooth(se=FALSE,method="lm")+theme_classic()+scale_color_manual(values=pal,name=expression(italic(T[c])))+theme(text = element_text(size=20))+theme(axis.line=element_line(size=1.4))
plA<-plA+xlab("year")+ylab(expression(italic(d[T[max]]>T[c])))

plB<-ggplot(data=diffDays,aes(V1,183*(V7-V5),col=as.factor(V2)))+geom_point()+geom_smooth(se=FALSE,method="lm")+theme_classic()+scale_color_manual(values=pal,name=expression(italic(T[c])))+theme(text = element_text(size=20))+theme(axis.line=element_line(size=1.4))
plB<-plB+xlab("year")+ylab(expression(italic(d[A]-d[a])))

plC<-ggplot(data=diffDays,aes(183*(V6-V4),183*(V7-V5),col=as.factor(V2)))+geom_point()+geom_smooth(se=FALSE,method="lm")+theme_classic()+scale_color_manual(values=pal,name=expression(italic(T[c])))+theme(text = element_text(size=20))+theme(axis.line=element_line(size=1.4))
plC<-plC+xlab(expression(italic(d[A]-d[a]) *" (Expected)"))+ylab(expression(italic(d[A]-d[a]) * " (Observed)"))
xy<-data.frame(x=seq(0,0.3,0.01),y=seq(0,0.3,0.01))
plC<-plC+geom_line(data=xy,aes(x,y),col="black",lty=2)

plot_grid(plA,plB,plC,labels=c("A","B","C"),ncol=3)  

ggsave("~/projects/Pigeon/Figures/diffDays.pdf",width=16,height=4)
            