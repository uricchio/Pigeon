library(ggplot2)
library(cowplot)
library(wesanderson)



# now the dA-da plot

read.table("~/projects/Pigeon/tempData/diff_dA_da.x_T.NY.txt")->diffDays

pal <- wes_palette("Zissou1",6,type="continuous")
plA<-ggplot(data=diffDays,aes(V1,V4,col=as.factor(V2)))+geom_point()+geom_smooth(se=FALSE,method="lm")+theme_classic()+scale_color_manual(values=pal,name=expression(italic(x[T])))+theme(text = element_text(size=20))+theme(axis.line=element_line(size=1.4))
plA<-plA+xlab("year")+ylab(expression(italic(d[T]>x[T])))

plB<-ggplot(data=diffDays,aes(V1,V7-V5,col=as.factor(V2)))+geom_point()+geom_smooth(se=FALSE,method="lm")+theme_classic()+scale_color_manual(values=pal,name=expression(italic(x[T])))+theme(text = element_text(size=20))+theme(axis.line=element_line(size=1.4))
plB<-plB+xlab("year")+ylab(expression(italic(d[A]-d[a])))

plC<-ggplot(data=diffDays,aes(V6-V4,V7-V5,col=as.factor(V2)))+geom_point()+geom_smooth(se=FALSE,method="lm")+theme_classic()+scale_color_manual(values=pal,name=expression(italic(x[T])))+theme(text = element_text(size=20))+theme(axis.line=element_line(size=1.4))
plC<-plC+xlab(expression(italic(d[A]-d[a]) *" (Expected)"))+ylab(expression(italic(d[A]-d[a]) * " (Observed)"))
xy<-data.frame(x=seq(0,0.2,0.01),y=seq(0,0.2,0.01))
plC<-plC+geom_line(data=xy,aes(x,y),col="black",lty=2)

plot_grid(plA,plB,plC,labels=c("A","B","C"),ncol=3)  

ggsave("~/projects/Pigeon/Figures/diffDays.NY.pdf",width=16,height=4)
