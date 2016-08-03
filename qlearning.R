# http://www.umiacs.umd.edu/~hal/courses/ai/out/cs421-day10-qlearning.pdf

# 0  0  0 +1
# 0 na  0 -1
# s  0  0  0

# Q=R+l*Q

l=0.8

R=rbind(c(NA,0,NA,0,NA,NA,NA,NA,NA,NA,NA),
        c(0,NA,0,NA,NA,NA,NA,NA,NA,NA,NA),
        c(NA,0,NA,NA,0,NA,NA,NA,NA,NA,NA),
        c(0,NA,NA,NA,NA,0,NA,NA,NA,NA,NA),
        c(NA,NA,0,NA,NA,NA,NA,0,NA,NA,NA),
        c(NA,NA,NA,0,NA,NA,NA,NA,0,NA,NA),
        c(NA,NA,NA,NA,NA,0,NA,0,NA,-1,NA),
        c(NA,NA,NA,NA,0,NA,0,NA,NA,NA,+1),
        c(NA,NA,NA,NA,NA,0,NA,NA,NA,-1,NA))

Q=rbind(c(NA,0,NA,0,NA,NA,NA,NA,NA,NA,NA),
        c(0,NA,0,NA,NA,NA,NA,NA,NA,NA,NA),
        c(NA,0,NA,NA,0,NA,NA,NA,NA,NA,NA),
        c(0,NA,NA,NA,NA,0,NA,NA,NA,NA,NA),
        c(NA,NA,0,NA,NA,NA,NA,0,NA,NA,NA),
        c(NA,NA,NA,0,NA,NA,NA,NA,0,NA,NA),
        c(NA,NA,NA,NA,NA,0,NA,0,NA,0,NA),
        c(NA,NA,NA,NA,0,NA,0,NA,NA,NA,0),
        c(NA,NA,NA,NA,NA,0,NA,NA,NA,0,NA),
        c(0,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA),
        c(0,NA,NA,NA,NA,NA,NA,NA,NA,NA,NA))

for(i in 1:50000){
  pos=1
  while(pos<10){
    temp<-Q[pos,]
    lis<-which(!is.na(temp),)
    temp<-temp[!is.na(temp)]+1
    temp<-cumsum(temp/sum(temp))>runif(1)
    pos1<-lis[length(temp[temp==FALSE])+1]
    expect<-Q[pos1,]
    expect<-expect[!is.na(expect)]
    Q[pos,pos1]<-R[pos,pos1]+l*sum(expect)/length(expect)
    pos<-pos1
  }
}
Q
