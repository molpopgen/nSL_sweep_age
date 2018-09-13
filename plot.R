library(lattice)
library(dplyr)

h=read.table("hard_sweeps_tau_z.txt",header=T) %>% mutate(f0="single origin")
s=read.table("soft_sweeps_tau_z.txt",header=T)

x = rbind(h,s)
lattice.theme <- trellis.par.get()
col <- lattice.theme$superpose.symbol$col
p = xyplot(mean_z ~ tau, data = x, group=as.factor(f0),
           type='l',
           lwd=3,
           key=list(text=list(levels(as.factor(x$f0))),
                    col=col,
                    lines=list(col=col[1:nlevels(as.factor(x$f0))]),
                   columns=3),# nlevels(as.factor(x$f0))),
           xlab=expression(paste(tau," (generations/4N)")),
           ylab="Mean z-score",
           panel=function(...){
               panel.xyplot(...)
               panel.abline(h=0.0,lty="dotted")
           }
           )

trellis.device(device="pdf",file="nSL_zscore.pdf",pointsize=18)
print(p)
dev.off()
#           auto.KEY=TRUE)

