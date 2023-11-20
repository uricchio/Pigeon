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



