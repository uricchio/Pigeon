library(ggplot2)
library(cowplot)
library(wesanderson)

read.table("~/projects/Pigeon/modelData/delQ.txt")->delQ


plA<-ggplot(delQ,aes(V2,V1,col=interaction(V3,V4)))+geom_line(lwd=1.1)+theme_classic()+xlab(expression("frequency of recessive allele (" * italic(q) * ")"))+
      ylab(expression("frequency change (" * Delta * italic(q) * ")" ))+scale_color_manual(values=wes_palette(("Darjeeling1")))+theme(axis.line=element_line(size=1.3))+
      theme(axis.text=element_text(size=12),axis.title = element_text(size=14))+theme(legend.position="none")
plA<-plA+geom_hline(yintercept=0,lty=2)

read.table("~/projects/Pigeon/modelData/DdelQ.txt")->DdelQ


plB<-ggplot(DdelQ,aes(V2,V1,col=interaction(V3,V4),linetype=as.factor(V5)))+geom_line(lwd=1.1)+theme_classic()+xlab(expression("selection strength (" * italic(s[a]) * ")"))+
  ylab(expression("rate of frequency change (" * frac(italic(d),italic(dq)) *  Delta * italic(q) * ")" ))+scale_color_manual(values=wes_palette(("Darjeeling1")),name=expression(italic(s[A]) * "." * italic(S[a])))+theme(axis.line=element_line(size=1.3))+
  theme(axis.text=element_text(size=12),axis.title = element_text(size=14))+ylim(-0.01,0.01)+guides(linetype=FALSE)
plB<-plB+geom_hline(yintercept=0,lty=2)

plB


plot_grid(plA, plB, labels=c("A","B"),ncol = 2,rel_widths=c(1,1.3))

ggsave("~/projects/Pigeon/ModelFig.pdf",height=3.7,width=13)
