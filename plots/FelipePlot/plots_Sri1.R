require("ggplot2")
require("dplyr")
require("tidyr")
require("ggthemes ")
require("latex2exp")
require("ggplot2")
require("plotly")
require("reshape")
require("zoo")
############MultiPlot fro GGPLOT#######################################################

multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
   library(grid)
   
   # Make a list from the ... arguments and plotlist
   plots <- c(list(...), plotlist)
   
   numPlots = length(plots)
   
   # If layout is NULL, then use 'cols' to determine layout
   if (is.null(layout)) {
      # Make the panel
      # ncol: Number of columns of plots
      # nrow: Number of rows needed, calculated from # of cols
      layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                       ncol = cols, nrow = ceiling(numPlots/cols))
   }
   
   if (numPlots==1) {
      print(plots[[1]])
      
   } else {
      # Set up the page
      grid.newpage()
      pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))
      
      # Make each plot, in the correct location
      for (i in 1:numPlots) {
         # Get the i,j matrix positions of the regions that contain this subplot
         matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))
         
         print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                         layout.pos.col = matchidx$col))
      }
   }
}



# Covariance plotting -----------------------------------------------------


covplot <- function(filename,title){
   Cov2020<-read.csv(filename, header = TRUE)
   Cov2020[upper.tri(Cov2020)] <- NA
   Cov_2020<-Cov2020 %>% gather(Producer2,Cov,-Producer)
   
   P_cov2020<-ggplot(Cov_2020, aes(y = Producer2, x = Producer,fill = Cov)) + geom_tile( colour = "black") +
      scale_fill_gradient2(low = "blue", high = "red", mid = "grey", na.value = "white", name = title,
      midpoint = 0,  limit = c(min(Cov_2020$Cov),max(Cov_2020$Cov)), space = "Lab")+ ylab("Producer")+
      theme(axis.text.x = element_text(angle = 90, hjust = 1), legend.key.width = unit(0.2,"cm")) +
      theme(axis.text.y = element_text(angle = 0, hjust = 1))
      #theme( legend.position = c(0.15,0.6), legend.direction = "vertical") 
}



C20 <- covplot(filename = "Cov_2020.csv",title ="2020")
C25 <- covplot(filename = "Cov_2025.csv",title ="2025")
C30 <- covplot(filename = "Cov_2030.csv",title ="2030")
C35 <- covplot(filename = "Cov_2035.csv",title ="2035")
C40 <- covplot(filename = "Cov_2040.csv",title ="2040")

CovPlotAll <- multiplot(C25,C35,cols=1)

# Random -------

C20
C25
C30
C35
C40





# Variance plotting -------------------------------------------------------

title = "Production"

filename = "v_Qpy_c1.csv"
#varplot <- function(filename,title){
Var<-read.csv(filename, header = FALSE)
names(Var) <- c(2020,2025,2030,2035,2040)
Producers = c("ALK","CAE","CAW","MEX2","MEX5","US2","US3","US4","US5","US6","US7","US8","US9")
Var <- cbind(Var,Producer=Producers)
Vardiv<-Var %>% gather(Year,Var,-Producer)

P_Var<-ggplot(Vardiv, aes(y = Producer, x = Year,fill = Var)) + geom_tile( colour = "black") +
   scale_fill_gradient2(low = "green", high = "red", mid = "grey", na.value = "white", name = paste("Std Dev:",title,sep="\n"),
                        midpoint = 0,  limit = c(min(Cov_2020$Cov),max(Cov_2020$Cov)), space = "Lab")

filename = "v_Qcy_c1.csv"
title = "Consumption"
Var<-read.csv(filename, header = FALSE)
names(Var) <- c(2020,2025,2030,2035,2040)
Var[17,"2040"] = 5
Consumers <- c("ALK","CAE","CAW","MEX1","MEX2","MEX3","MEX4","MEX5","US1","US2","US3","US4","US5","US6","US7","US8","US9")
Var <- cbind(Var,Consumer = Consumers)
Vardiv<-Var %>% gather(Year,Var,-Consumer)
C_Var<-ggplot(Vardiv, aes(y = Consumer, x = Year,fill = Var)) + geom_tile( colour = "black") +
   scale_fill_gradient2(low = "green", high = "red", mid = "grey", na.value = "white", name = paste("Std Dev:",title,sep="\n"),
                        midpoint = 0,  limit = c(min(Cov_2020$Cov),max(Cov_2020$Cov)), space = "Lab")
C_Var
multiplot(P_Var,C_Var)


####### Sensitivity ------------

T = read.csv('T_small.csv',header=FALSE)
x = read.csv('x_small.csv',header=FALSE)
StochA = read.csv('StochA.csv',header=FALSE)
T^2 -> B1

### Relative Sensitivity

# Production/Production
P_P_T <- T[211:301,428:518]/as.vector(x[211:301,])
P_P_B1 <- P_P_T^2
P_P_B2 <- colSums(P_P_B1)
temp<-matrix(as.vector(sqrt(P_P_B2)*StochA[428:518,]/100),13,7,byrow=TRUE)[,c(-1,-2)]
P_P <- data.frame(cbind(Producers,temp/sum(temp)))
names(P_P)<-c("Producer","2020","2025","2030","2035","2040")
P.P <- P_P %>% gather(Year,Sensitivity,-Producer)
P.P$Sensitivity <- as.numeric(P.P$Sensitivity)
P_Var<-ggplot(P.P, aes(y = Producer, x = Year,fill = Sensitivity)) + geom_tile( colour = "black") +
      scale_fill_gradient2(low = "green", high = "red", mid = "grey", na.value = "white", name = "Relative sensitivity\nProduction/Production",
                        midpoint = 0,   space = "Lab")


# Consumption/Production
C_P_T <- T[211:301,8:126]/as.vector(x[211:301,])
C_P_B1 <- C_P_T^2
C_P_B2 <- colSums(C_P_B1)
temp<-matrix(as.vector(sqrt(C_P_B2)*StochA[8:126,]/100),17,7,byrow=TRUE)[,c(-1,-2)]
C_P <- data.frame(cbind(Consumers,temp/sum(temp)))
names(C_P)<-c("Consumer","2020","2025","2030","2035","2040")
C.P <- C_P %>% gather(Year,Sensitivity,-Consumer)
C.P$Sensitivity <- as.numeric(C.P$Sensitivity)
C_Var<-ggplot(C.P, aes(y = Consumer, x = Year,fill = Sensitivity)) + geom_tile( colour = "black") +
   scale_fill_gradient2(low = "green", high = "red", mid = "grey", na.value = "white", name = "Relative sensitivity\nProduction/Production",
                        midpoint = 0,   space = "Lab")


### Absolute Sensitivity
 
# Production/Production
P_P_T <- T[211:301,428:518]
P_P_B1 <- P_P_T^2
P_P_B2 <- colSums(P_P_B1)
temp<-matrix(as.vector(sqrt(P_P_B2)*StochA[428:518,]/100),13,7,byrow=TRUE)[,c(-1,-2)]
P_P <- data.frame(cbind(Producers,temp))
names(P_P)<-c("Producer","2020","2025","2030","2035","2040")
P.P <- P_P[-2,] %>% gather(Year,Sensitivity,-Producer)
P.P$Sensitivity <- as.numeric(P.P$Sensitivity)
P_Varabs <- ggplot(P.P, aes(y = Producer, x = Year,fill = Sensitivity)) + geom_tile( colour = "black") +
   scale_fill_gradient2(low = "green", high = "#FF0000", mid = "grey", na.value = "white", name = "Absolute sensitivity\nProduction/Production",
                        midpoint = 0,  space = "Lab")


# Consumption/Production
C_P_T <- T[211:301,8:126]
C_P_B1 <- C_P_T^2
C_P_B2 <- colSums(C_P_B1)
temp<-matrix(as.vector(sqrt(C_P_B2)*StochA[8:126,]/100),17,7,byrow=TRUE)[,c(-1,-2)]
C_P <- data.frame(cbind(Consumers,temp))
names(C_P)<-c("Consumer","2020","2025","2030","2035","2040")
C.P <- C_P[-1,] %>% gather(Year,Sensitivity,-Consumer)
C.P$Sensitivity <- as.numeric(C.P$Sensitivity)
C_Varabs<-ggplot(C.P, aes(y = Consumer,  x = Year,fill = Sensitivity)) + geom_tile( colour = "black") +
   scale_fill_gradient2(low = "green", high = "red", mid = "grey", na.value = "white", name = "Absolute sensitivity\nProduction/Consumption",
                        midpoint = 00, limit = c(0,15000),  space = "Lab")

P_Varabs
C_Varabs


# Comparative Sensitivity and Tornado plot
B2 <- colSums(B1)
B2rel <- as.vector(t(B2*StochA/100))
# plot(1:2023,B2rel)
#  
# df.s	   	<- sum(B2[1:7   ])
# DemSlope.s	<- sum(B2[8:126 ])
# DemInt.s	   <- sum(B2[127:245 ])
# CostP.s		<- sum(B2[246:336 ])
# CostQ.s		<- sum(B2[337:427 ])
# CostG.s		<- sum(B2[428:518 ])
# CostA.s		<- sum(B2[519:959 ])
# PIXP.s		<- sum(B2[960:1050])
# PIXA.s		<- sum(B2[1051:1491])
# LossP.s		<- sum(B2[1492:1582])
# LossA.s		<- sum(B2[1583:2023])
# 
# sum(df.s,DemSlope.s,DemInt.s,CostP.s,CostQ.s,CostG.s,CostA.s,PIXP.s,PIXA.s,LossP.s,LossA.s) -> Tot.s
# df.s =  df.s/Tot.s
# DemSlope.s =  DemSlope.s/Tot.s
# DemInt.s =  DemInt.s/Tot.s
# CostP.s =  CostP.s/Tot.s
# CostQ.s =  CostQ.s/Tot.s
# CostG.s =  CostG.s/Tot.s
# CostA.s =  CostA.s/Tot.s
# PIXP.s =  PIXP.s/Tot.s
# PIXA.s =  PIXA.s/Tot.s
# LossP.s =  LossP.s/Tot.s
# LossA.s =  LossA.s/Tot.s
# 
# dat <- data.frame(
#    Parameters = c(
#       "Discount Factors",
#       "Slope of demand curve",
#       "Intercept of demand curve",
#       "Linear production cost parameter",
#       "Quadratic production cost parameter",
#       "Golembek production cost parameter",
#       "Cost of Transportation",
#       "Cost of production expansion",
#       "Cost of pipeline construction",
#       "Production loss",
#       "Transport loss"
#    ),
#    value = c(
#       df.s,
#       DemSlope.s,
#       DemInt.s,
#       CostP.s,
#       CostQ.s,
#       CostG.s,
#       CostA.s,
#       PIXP.s,
#       PIXA.s,
#       LossP.s,
#       LossA.s
#    )
# )
# # Sorting for Tornado plot
# dat$Parameters <- factor(dat$Parameters, levels = dat$Parameters[order(dat$value)])
# ggplot(dat,aes(Parameters,value))+ coord_flip() + geom_bar(position = "identity",stat = "identity")  + theme(axis.text.x = element_text(angle = 0, hjust = 0.5))  + scale_y_log10()





df.s.rel	   	<- sum(B2rel[1:7   ])
DemSlope.s.rel	<- sum(B2rel[8:126 ])
DemInt.s.rel	   <- sum(B2rel[127:245 ])
CostP.s.rel		<- sum(B2rel[246:336 ])
CostQ.s.rel		<- sum(B2rel[337:427 ])
CostG.s.rel		<- sum(B2rel[428:518 ])
CostA.s.rel		<- sum(B2rel[519:959 ])
PIXP.s.rel		<- sum(B2rel[960:1050])
PIXA.s.rel		<- sum(B2rel[1051:1491])
LossP.s.rel		<- sum(B2rel[1492:1582])
LossA.s.rel		<- sum(B2rel[1583:2023])

# sum(df.s.rel,DemSlope.s.rel,DemInt.s.rel,CostP.s.rel,CostQ.s.rel,CostG.s.rel,CostA.s.rel,PIXP.s.rel,PIXA.s.rel,LossP.s.rel,LossA.s.rel) -> Tot.s.rel

# df.s.rel =  df.s.rel/Tot.s.rel
# DemSlope.s.rel =  DemSlope.s.rel/Tot.s.rel
# DemInt.s.rel =  DemInt.s.rel/Tot.s.rel
# CostP.s.rel =  CostP.s.rel/Tot.s.rel
# CostQ.s.rel =  CostQ.s.rel/Tot.s.rel
# CostG.s.rel =  CostG.s.rel/Tot.s.rel
# CostA.s.rel =  CostA.s.rel/Tot.s.rel
# PIXP.s.rel =  PIXP.s.rel/Tot.s.rel
# PIXA.s.rel =  PIXA.s.rel/Tot.s.rel
# LossP.s.rel =  LossP.s.rel/Tot.s.rel
# LossA.s.rel =  LossA.s.rel/Tot.s.rel

dat <- data.frame(
   Parameters = c(
      "Discount Factors",
      "Slope of \ndemand curve",
      "Intercept of \ndemand curve",
      "Linear cost \nparameter",
      "Quadratic cost \nparameter",
      "Golembek cost \nparameter",
      "Transportation \ncost",
      "Production \nexpansion cost",
      "Pipeline \nconstruction cost"
   ),
   Sensitivity = log10(c(
      df.s.rel,
      DemSlope.s.rel,
      DemInt.s.rel,
      CostP.s.rel,
      CostQ.s.rel,
      CostG.s.rel,
      CostA.s.rel,
      PIXP.s.rel,
      PIXA.s.rel
   ))
)
# Sorting for Tornado plot
dat$Parameters <- factor(dat$Parameters, levels = dat$Parameters[order(dat$Sensitivity)])
number_ticks <- function(n) {function(limits) pretty(limits, n)}
ggplot(dat,aes(Parameters,Sensitivity))+ coord_flip() + geom_bar(fill = "blue",position = "identity",stat = "identity") +labs(y = "Log Sensitivity")+ scale_y_continuous(breaks = number_ticks(8))  + theme(axis.text.y = element_text(angle = 0, hjust = 1))  #+ scale_y_log10()


