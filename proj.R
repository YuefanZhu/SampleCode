library(scales)
library(dplyr)
library(ggplot2)
library(reshape2)
df=read.csv('C:/Users/yz283/Desktop/proj/YUE.csv',header=TRUE,sep=',',stringsAsFactors=FALSE)
df1=read.csv('C:/Users/yz283/Desktop/proj/Ver_26.csv',header=TRUE,sep=',',stringsAsFactors=FALSE)
Rate=read.csv('C:/Users/yz283/Desktop/proj/TbillRate.csv',header=TRUE,sep=',',stringsAsFactors=FALSE)
Rate=Rate[c('X','X.2')]
Rate=Rate[2:nrow(Rate),]
colnames(Rate)=c('TradeDate','Rate')
Rate$TradeDate=as.Date(Rate$TradeDate,'%m/%d/%Y')
df$TradeDate=as.Date(df$TradeDate,'%m/%d/%Y')
df1$TradeDate=as.Date(df1$TradeDate,'%m/%d/%Y')
df1['Gold']=df1['Fut']*120000
df1['Aurum']=df1['Fut']*120000+df1['PnL']
mydf=df1[c('TradeDate','Aurum','Gold')]
mydf=mydf[order(mydf$TradeDate),]
# format(df$TradeDate,'%Y')
# Subset the last date for each month
m <- data.frame()
for (i in 1:(nrow(mydf)-1)){
  if(as.numeric(format(mydf['TradeDate'][i+1,],'%d'))<as.numeric(format(mydf['TradeDate'][i,],'%d'))){
    m <- rbind(m,mydf[i,])
  }
}
mat=cbind(m$TradeDate[2:nrow(m)],diff(m$Aurum)/m$Aurum[1:(nrow(m)-1)],diff(m$Gold)/m$Gold[1:(nrow(m)-1)])
mat=data.frame(mat)
colnames(mat)=c('TradeDate','Aurum','Gold')
mat$TradeDate=as.Date(mat$TradeDate,origin="1970-01-01")


# Subset the last date for each year
y <- data.frame()
for (i in 1:(nrow(mydf)-1)){
  if(as.numeric(format(mydf['TradeDate'][i+1,],'%m'))<as.numeric(format(mydf['TradeDate'][i,],'%m'))){
    y <- rbind(y,mydf[i,])
  }
}
mat1=cbind(y$TradeDate[2:nrow(y)],diff(y$Aurum)/y$Aurum[1:(nrow(y)-1)],diff(y$Gold)/y$Gold[1:(nrow(y)-1)])
mat1=data.frame(mat1)
colnames(mat1)=c('TradeDate','Aurum','Gold')
mat1$TradeDate=as.Date(mat1$TradeDate,origin="1970-01-01")

ot=rbind(mat,mat1)
#write.csv(ot,'C:/Users/yz283/Desktop/proj/ot.csv')
mat2=cbind(q$TradeDate[2:nrow(q)],diff(q$Aurum)/q$Aurum[1:(nrow(q)-1)],diff(q$Gold)/q$Gold[1:(nrow(q)-1)])
mat2=data.frame(mat2)
colnames(mat2)=c('TradeDate','Aurum','Gold')
mat2$TradeDate=as.Date(mat2$TradeDate,origin="1970-01-01")



# Subset the last date for each quarter
q <- data.frame()
for (i in 1:(nrow(mydf)-1)){
  if(as.numeric(format(mydf['TradeDate'][i+1,],'%d'))<as.numeric(format(mydf['TradeDate'][i,],'%d')) & as.numeric(format(mydf['TradeDate'][i,],'%m')) %in% c(3,6,9,12)){
    q <- rbind(q,mydf[i,])
  }
}

#write.csv(y,'C:/Users/yz283/Desktop/proj/year.csv')
#write.csv(m,'C:/Users/yz283/Desktop/proj/month.csv')
#write.csv(q,'C:/Users/yz283/Desktop/proj/quarter.csv')

# daily stat
(mydf[c('Aurum','Gold')][nrow(mydf),]/mydf[c('Aurum','Gold')][1,])^(1/(nrow(mydf)/252))-1
mydf[c('Aurum','Gold')][nrow(mydf),]/mydf[c('Aurum','Gold')][1,]-1
maxD=c(0,0)
# for (i in 1:(nrow(mydf)-1)){
#   for(j in (i+1):nrow(mydf)){
#    if ((mydf$Aurum[j]-mydf$Aurum[i])/mydf$Aurum[i]<maxD[1]){
#       maxD[1]=(mydf$Aurum[j]-mydf$Aurum[i])/mydf$Aurum[i]
#     }
#     if ((mydf$Gold[j]-mydf$Gold[i])/mydf$Gold[i]<maxD[2]){
#       maxD[2]=(mydf$Gold[j]-mydf$Gold[i])/mydf$Gold[i]
#     }
#   }
# }

r=cbind(mydf$TradeDate[2:nrow(mydf)],log(mydf$Aurum[2:nrow(mydf)]/mydf$Aurum[1:(nrow(mydf)-1)]),log(mydf$Gold[2:nrow(mydf)]/mydf$Gold[1:(nrow(mydf)-1)]))
r=data.frame(r)
colnames(r)=c('TradeDate','Aurum','Gold')
r$TradeDate=as.Date(r$TradeDate,origin="1970-01-01")
r<-r %>% left_join(Rate,by = c("TradeDate"))
for (i in 1:nrow(r)){
  if(is.na(r$Rate[i]) | r$Rate[i]=="N/A"){
    r$Rate[i]=r$Rate[i-1]
  }
}
r$Rate=log(as.numeric(r$Rate)/100+1)/252
r$AurumR=r$Aurum-r$Rate
r$GoldR=r$Gold-r$Rate
# Sharpe
mean(r$AurumR)/sd(r$AurumR)*sqrt(252)
mean(r$GoldR)/sd(r$GoldR)*sqrt(252)
# Sortino
r$ASor=r$AurumR
r$GSor=r$GoldR
for (i in 1:nrow(r)){
  r$ASor[i]=min(0,r$ASor[i])
  r$GSor[i]=min(0,r$GSor[i])
}
mean(r$AurumR)/sd(r$ASor)*sqrt(252)
mean(r$GoldR)/sd(r$GSor)*sqrt(252)
# Monthly Sd & Yearly Sd
msd=m[2:nrow(m),2:3]/m[1:(nrow(m)-1),2:3]-1
sd(msd$Aurum)
sd(msd$Gold)
ysd=y[2:nrow(y),2:3]/y[1:(nrow(y)-1),2:3]-1
sd(ysd$Aurum)
sd(ysd$Gold)
# corr
posit_m=subset(msd,msd$Aurum>0)
nega_m=subset(msd,msd$Aurum<0)
posit_y=subset(ysd,ysd$Aurum>0)
nega_y=subset(ysd,ysd$Aurum<0)
cov(posit_m$Aurum,posit_m$Gold)/sd(posit_m$Aurum)/sd(posit_m$Gold)
cov(nega_m$Aurum,nega_m$Gold)/sd(nega_m$Aurum)/sd(nega_m$Gold)
cov(posit_y$Aurum,posit_y$Gold)/sd(posit_y$Aurum)/sd(posit_y$Gold)
cov(nega_y$Aurum,nega_y$Gold)/sd(nega_y$Aurum)/sd(nega_y$Gold)

# Monthly sharpe $ Sortino
r=cbind(m$TradeDate[2:nrow(m)],log(m$Aurum[2:nrow(m)]/m$Aurum[1:(nrow(m)-1)]),log(m$Gold[2:nrow(m)]/m$Gold[1:(nrow(m)-1)]))
r=data.frame(r)
colnames(r)=c('TradeDate','Aurum','Gold')
r$TradeDate=as.Date(r$TradeDate,origin="1970-01-01")
r<-r %>% left_join(Rate,by = c("TradeDate"))
for (i in 1:nrow(r)){
  if(is.na(r$Rate[i]) | r$Rate[i]=="N/A"){
    r$Rate[i]=r$Rate[i-1]
  }
}
r$Rate=log(as.numeric(r$Rate)/100+1)/12
r$AurumR=r$Aurum-r$Rate
r$GoldR=r$Gold-r$Rate
# Sharpe
mean(r$AurumR)/sd(r$AurumR)*sqrt(12)
mean(r$GoldR)/sd(r$GoldR)*sqrt(12)
# Sortino
r$ASor=r$AurumR
r$GSor=r$GoldR
for (i in 1:nrow(r)){
  r$ASor[i]=min(0,r$ASor[i])
  r$GSor[i]=min(0,r$GSor[i])
}
mean(r$AurumR)/sd(r$ASor)*sqrt(12)
mean(r$GoldR)/sd(r$GSor)*sqrt(12)
# Annualized Sd
sd(r$Aurum)*sqrt(12)
sd(r$Gold)*sqrt(12)

# Yearly sharpe $ Sortino
r=cbind(y$TradeDate[2:nrow(y)],log(y$Aurum[2:nrow(y)]/y$Aurum[1:(nrow(y)-1)]),log(y$Gold[2:nrow(y)]/y$Gold[1:(nrow(y)-1)]))
r=data.frame(r)
colnames(r)=c('TradeDate','Aurum','Gold')
r$TradeDate=as.Date(r$TradeDate,origin="1970-01-01")
r<-r %>% left_join(Rate,by = c("TradeDate"))
for (i in 1:nrow(r)){
  if(is.na(r$Rate[i]) | r$Rate[i]=="N/A"){
    r$Rate[i]=r$Rate[i-1]
  }
}
r$Rate=log(as.numeric(r$Rate)/100+1)
r$AurumR=r$Aurum-r$Rate
r$GoldR=r$Gold-r$Rate
# Sharpe
mean(r$AurumR)/sd(r$AurumR)*sqrt(1)
mean(r$GoldR)/sd(r$GoldR)*sqrt(1)
# Sortino
r$ASor=r$AurumR
r$GSor=r$GoldR
for (i in 1:nrow(r)){
  r$ASor[i]=min(0,r$ASor[i])
  r$GSor[i]=min(0,r$GSor[i])
}
mean(r$AurumR)/sd(r$ASor)*sqrt(1)
mean(r$GoldR)/sd(r$GSor)*sqrt(1)
# Annualized Sd
sd(r$Aurum)*sqrt(1)
sd(r$Gold)*sqrt(1)

# Quarterly sharpe $ Sortino
r=cbind(q$TradeDate[2:nrow(q)],log(q$Aurum[2:nrow(q)]/q$Aurum[1:(nrow(q)-1)]),log(q$Gold[2:nrow(q)]/q$Gold[1:(nrow(q)-1)]))
r=data.frame(r)
colnames(r)=c('TradeDate','Aurum','Gold')
r$TradeDate=as.Date(r$TradeDate,origin="1970-01-01")
r<-r %>% left_join(Rate,by = c("TradeDate"))
for (i in 1:nrow(r)){
  if(is.na(r$Rate[i]) | r$Rate[i]=="N/A"){
    r$Rate[i]=r$Rate[i-1]
  }
}
r$Rate=log(as.numeric(r$Rate)/100+1)/4
r$AurumR=r$Aurum-r$Rate
r$GoldR=r$Gold-r$Rate
# Sharpe
mean(r$AurumR)/sd(r$AurumR)*sqrt(4)
mean(r$GoldR)/sd(r$GoldR)*sqrt(4)
# Sortino
r$ASor=r$AurumR
r$GSor=r$GoldR
for (i in 1:nrow(r)){
  r$ASor[i]=min(0,r$ASor[i])
  r$GSor[i]=min(0,r$GSor[i])
}
mean(r$AurumR)/sd(r$ASor)*sqrt(4)
mean(r$GoldR)/sd(r$GSor)*sqrt(4)
# Annualized Sd
sd(r$Aurum)*sqrt(4)
sd(r$Gold)*sqrt(4)


# Graphs VAMIs
vm=m
vq=q
vy=y
vm$Aurum=vm$Aurum/vm$Aurum[1]*1000
vq$Aurum=vq$Aurum/vq$Aurum[1]*1000
vy$Aurum=vy$Aurum/vy$Aurum[1]*1000
vm$Gold=vm$Gold/vm$Gold[1]*1000
vq$Gold=vq$Gold/vq$Gold[1]*1000
vy$Gold=vy$Gold/vy$Gold[1]*1000

ggplot(vm, aes(TradeDate)) + 
  geom_line( aes(y = Aurum, colour = "Aurum")) + 
  geom_line( aes(y = Gold, colour = "Gold")) +
  xlab("Months") + ylab("VAMI") +
  scale_colour_hue(name="Color") + theme_bw() +
  theme(axis.line = element_line(colour = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_blank()) 

ggplot(vq, aes(TradeDate)) + 
  geom_line( aes(y = Aurum, colour = "Aurum")) + 
  geom_line( aes(y = Gold, colour = "Gold")) +
  xlab("Quarters") + ylab("VAMI") +
  scale_colour_hue(name="Color") + theme_bw() +
  theme(axis.line = element_line(colour = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_blank()) 

ggplot(vy, aes(TradeDate)) + 
  geom_line( aes(y = Aurum, colour = "Aurum")) + 
  geom_line( aes(y = Gold, colour = "Gold")) +
  xlab("Years") + ylab("VAMI") +
  scale_colour_hue(name="Color") + theme_bw() +
  theme(axis.line = element_line(colour = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_blank()) 

# Graphs returns
rm=mat
rm=rbind(cbind(rm$TradeDate,rm$Aurum,"Aurum"),cbind(rm$TradeDate,rm$Gold,"Gold"))
rm=data.frame(rm)
colnames(rm)=c('Date','Returns','Variable')
rm$Date=as.numeric(levels(rm$Date))[rm$Date]
rm$Date=as.Date(rm$Date,origin="1970-01-01")
rm$Returns=as.numeric(as.character(rm$Returns))
ggplot(data=rm, aes(x=Date, y=Returns, fill=Variable)) + 
  geom_bar(stat= "identity", position=position_dodge()) +
  xlab("Months") + ylab("Monthly Return") +
  scale_colour_hue(name="Color") + theme_bw() +
  theme(axis.line = element_line(colour = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_blank()) 

rm=mat
rm$TradeDate=NULL
rm=rm[order(rm$Gold),]
rm=rbind(cbind(rm$Aurum,"Aurum"),cbind(rm$Gold,"Gold"))
rm=data.frame(rm)
colnames(rm)=c('Returns','Variable')
rm$Returns=as.numeric(as.character(rm$Returns))
rm$id=rep(1:(nrow(rm)/2),2)
ggplot(data=rm, aes(x=id , y=Returns, fill=Variable)) + 
  geom_bar(stat= "identity", position=position_dodge()) +
  xlab("Months") + ylab("Sorted Monthly Return") +
  scale_colour_hue(name="Color") + theme_bw() +
  theme(axis.line = element_line(colour = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_blank()) 

rm=mat1
rm=rbind(cbind(rm$TradeDate,rm$Aurum,"Aurum"),cbind(rm$TradeDate,rm$Gold,"Gold"))
rm=data.frame(rm)
colnames(rm)=c('Date','Returns','Variable')
rm$Date=as.numeric(levels(rm$Date))[rm$Date]
rm$Date=as.Date(rm$Date,origin="1970-01-01")
rm$Returns=as.numeric(as.character(rm$Returns))
ggplot(data=rm, aes(x=Date, y=Returns, fill=Variable)) + 
  geom_bar(stat= "identity", position=position_dodge()) +
  xlab("Years") + ylab("Annually Return") +
  scale_colour_hue(name="Color") + theme_bw() +
  theme(axis.line = element_line(colour = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_blank()) 
rm=mat1
rm$TradeDate=NULL
rm=rm[order(rm$Gold),]
rm=rbind(cbind(rm$Aurum,"Aurum"),cbind(rm$Gold,"Gold"))
rm=data.frame(rm)
colnames(rm)=c('Returns','Variable')
rm$Returns=as.numeric(as.character(rm$Returns))
rm$id=rep(1:(nrow(rm)/2),2)
ggplot(data=rm, aes(x=id , y=Returns, fill=Variable)) + 
  geom_bar(stat= "identity", position=position_dodge()) +
  xlab("Years") + ylab("Sorted Annually Return") +
  scale_colour_hue(name="Color") + theme_bw() +
  theme(axis.line = element_line(colour = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_blank()) 

rm=mat2
rm=rbind(cbind(rm$TradeDate,rm$Aurum,"Aurum"),cbind(rm$TradeDate,rm$Gold,"Gold"))
rm=data.frame(rm)
colnames(rm)=c('Date','Returns','Variable')
rm$Date=as.numeric(levels(rm$Date))[rm$Date]
rm$Date=as.Date(rm$Date,origin="1970-01-01")
rm$Returns=as.numeric(as.character(rm$Returns))
ggplot(data=rm, aes(x=Date, y=Returns, fill=Variable)) + 
  geom_bar(stat= "identity", position=position_dodge()) +
  xlab("Quarters") + ylab("Quarterly Return") +
  scale_colour_hue(name="Color") + theme_bw() +
  theme(axis.line = element_line(colour = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_blank())

rm=mat2
rm$TradeDate=NULL
rm=rm[order(rm$Gold),]
rm=rbind(cbind(rm$Aurum,"Aurum"),cbind(rm$Gold,"Gold"))
rm=data.frame(rm)
colnames(rm)=c('Returns','Variable')
rm$Returns=as.numeric(as.character(rm$Returns))
rm$id=rep(1:(nrow(rm)/2),2)
ggplot(data=rm, aes(x=id , y=Returns, fill=Variable)) + 
  geom_bar(stat= "identity", position=position_dodge()) +
  xlab("Quarters") + ylab("Sorted Quarterly Return") +
  scale_colour_hue(name="Color") + theme_bw() +
  theme(axis.line = element_line(colour = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_blank()) 

# Strikes
