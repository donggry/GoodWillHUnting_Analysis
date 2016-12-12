library(aod)
library(ggplot2)
library(Rcpp)
library(RMySQL)

mydb = dbConnect(MySQL(), user='rnduser', password='hongik_gwh', dbname='falling', host='52.79.138.56')

#dbListTables(mydb)
#dbListFields(mydb, 'RelationView')
#rs = dbSendQuery(mydb,"select relationId,gbByMindCount.relMatchStatus,U.userId, U.gender, TU.gender,U.age, TU.age,CASE When U.age-TU.age>0 and U.age-TU.age<=5 Then '1' When U.age-TU.age<0 and U.age-TU.age>=-5 then '-1' When U.age-TU.age>5 and U.age-TU.age<=10 Then '2' When U.age-TU.age>10 then '3' When U.age-TU.age>=-10 and U.age-TU.age<-5 then '-2' When U.age-TU.age<-10 then '-3' When U.age-TU.age=0 Then '0' END as agegrade, U.countryCode, TU.countryCode,CASE When TimestampDiff(minute,U.fallingStartDate,TU.fallingStartDate)<=10 and TimestampDiff(minute,U.fallingStartDate,TU.fallingStartDate)>0 Then '0' When TimestampDiff(minute,U.fallingStartDate,TU.fallingStartDate)>60 and TimestampDiff(minute,U.fallingStartDate,TU.fallingStartDate)<=1440 Then '1'ELSE '2' END as Timegrade,U.fallingStartDate, TU.fallingStartDate, U.invitedDateByTarget, TU.invitedDateByTarget, U.facebookFriendsCount, TU.facebookFriendsCount, U.emotionId, TU.emotionId, matchDate, inviteCheck, CASE When countmind=0 Then '0'  ELSE '1'END as CountMind, hintCheckStatus, foundCheckStatus, CASE When countdiary=0 Then '0' ELSE '1'END as CountDiary from (select M.foundCheck foundCheckStatus, M.hintCheck hintCheckStatus, R.mainUserId mainUserId,R.matchDate, R.inviteCheck, R.relId relationId, R.targetUserId,COUNT(M.mindId) countmind ,R.matchCheck relMatchStatus,COUNT(D.diaryId) countdiary from (RelationView R LEFT OUTER JOIN MindView M ON R.relId=M.relId) LEFT OUTER JOIN DiaryView D ON R.relId=D.relId group by R.relId) as gbByMindCount JOIN UserView as U on gbByMindCount.mainUserId=U.userId JOIN UserView as TU ON TU.userId=gbByMindCount.targetUserId where U.age is not NULL and TU.age is not NULL")
rs = dbSendQuery(mydb,"select relationId,gbByMindCount.relMatchStatus,U.userId, U.gender, TU.gender,U.age, TU.age, CASE When U.age-TU.age>0 and U.age-TU.age<=5 Then '1' When U.age-TU.age<0 and U.age-TU.age>=-5 then '-1' When U.age-TU.age>5 and U.age-TU.age<=10 Then '2' When U.age-TU.age>10 then '3' When U.age-TU.age>=-10 and U.age-TU.age<-5 then '-2' When U.age-TU.age<-10 then '-3' When U.age-TU.age=0 Then '0' END as agegrade, U.countryCode, TU.countryCode,CASE When TimestampDiff(minute,U.fallingStartDate,TU.fallingStartDate)<=10 and TimestampDiff(minute,U.fallingStartDate,TU.fallingStartDate)>0 Then '0' When TimestampDiff(minute,U.fallingStartDate,TU.fallingStartDate)>60 and TimestampDiff(minute,U.fallingStartDate,TU.fallingStartDate)<=1440 Then '1'ELSE '2' END as Timegrade,U.fallingStartDate, TU.fallingStartDate, U.invitedDateByTarget, TU.invitedDateByTarget, U.facebookFriendsCount, TU.facebookFriendsCount, U.emotionId, TU.emotionId, matchDate, inviteCheck, CASE When countmind=0 Then '0' ELSE '1'END mindcount, hintCheckStatus, foundCheckStatus, CASE When countdiary=0 Then '0' ELSE '1'END as diarycount from (select M.foundCheck foundCheckStatus, M.hintCheck hintCheckStatus, R.mainUserId mainUserId,R.matchDate, R.inviteCheck, R.relId relationId, R.targetUserId,COUNT(M.mindId) countmind ,R.matchCheck relMatchStatus,COUNT(D.diaryId) countdiary from (RelationView R LEFT OUTER JOIN MindView M ON R.relId=M.relId) LEFT OUTER JOIN DiaryView D ON R.relId=D.relId group by R.relId) as gbByMindCount JOIN UserView as U on gbByMindCount.mainUserId=U.userId JOIN UserView as TU ON TU.userId=gbByMindCount.targetUserId where U.age is not NULL and TU.age is not NULL")

#select relationId,gbByMindCount.relMatchStatus, U.gender, TU.gender,U.age, TU.age,U.age-TU.age as agegrade, U.countryCode, TU.countryCode,TimestampDiff(hour,U.fallingStartDate,TU.fallingStartDate) as Timegrade, U.fallingStartDate, TU.fallingStartDate, U.invitedDateByTarget, TU.invitedDateByTarget, U.facebookFriendsCount, TU.facebookFriendsCount, U.emotionId, TU.emotionId, matchDate, inviteCheck, countMind, hintCheckStatus, foundCheckStatus  from (select M.foundCheck foundCheckStatus, M.hintCheck hintCheckStatus, R.mainUserId mainUserId,R.matchDate, R.inviteCheck, R.relId relationId, R.targetUserId, COUNT(M.mindId) countMind,R.matchCheck relMatchStatus from RelationView R LEFT OUTER JOIN MindView M ON R.relId=M.relId group by R.relId) as gbByMindCount JOIN UserView as U on gbByMindCount.mainUserId=U.userId JOIN UserView as TU ON TU.userId=gbByMindCount.targetUserId")

data = fetch(rs, n=-1)
write.csv(data,"mydata10.csv")
mydata <- read.csv("mydata10.csv")
#mydata <-read.csv("xtabtest.csv")
## view the first few rows of the data
head(mydata)

summary(mydata)

sapply(mydata, sd)

## two-way contingency table of categorical outcome and predictors
## we want to make sure there are not 0 cells
#xtabs(~ relMatchStatus +Timegrade+ agegrade+hintCheckStatus+foundCheckStatus, data = mydata)
xtabs(~ relMatchStatus +gender+agegrade+Timegrade+mindcount+hintCheckStatus+foundCheckStatus+diarycount, data = mydata)

mydata$gender <- factor(mydata$gender)
mydata$agegrade <- factor(mydata$agegrade)
mydata$Timegrade <- factor(mydata$Timegrade)
mydata$mindcount <- factor(mydata$mindcount)
mydata$hintCheckStatus <- factor(mydata$hintCheckStatus)
mydata$foundCheckStatus<- factor(mydata$foundCheckStatus)
mydata$relMatchStatus <- factor(mydata$relMatchStatus)
mydata$diarycount <- factor(mydata$diarycount)
mydata$mindcount

mylogit <- glm(relMatchStatus ~ +mindcount+gender+agegrade+Timegrade+diarycount, data = mydata, family = "binomial") ## X2 = 7.1, df = 5, P(> X2) = 0.21
wald.test(b = coef(mylogit), Sigma = vcov(mylogit), Terms = 2:6)
mylogit <- glm(relMatchStatus ~ +gender+agegrade+Timegrade+hintCheckStatus+foundCheckStatus+mindcount+diarycount, data = mydata, family = "binomial" ) 
## X2 = 7.1, df = 5, P(> X2) = 0.21
#mylogit <- glm(relMatchStatus ~ + gender+agegrade+hintCheckStatus+foundCheckStatus+CountDiary, data = mydata, family = "binomial")## X2 = 14.6, df = 5, P(> X2) = 0.012
#mylogit <- glm(relMatchStatus ~ + gender+Timegrade+CountMind+hintCheckStatus+foundCheckStatus+CountDiary, data = mydata, family = "binomial") ## X2 = 25.7, df = 6, P(> X2) = 0.00025->>0.27로 떨어짐...
#mylogit <- glm(relMatchStatus ~ + gender+agegrade+Timegrade+hintCheckStatus+foundCheckStatus+CountDiary, data = mydata, family = "binomial")## X2 = 7.8, df = 6, P(> X2) = 0.26
#mylogit <- glm(relMatchStatus ~ +agegrade+CountMind+hintCheckStatus+foundCheckStatus+CountDiary, data = mydata, family = "binomial") ## X2 = 13.8, df = 5, P(> X2) = 0.017

summary(mylogit)

## CIs using profiled log-likelihood
confint(mylogit)
## CIs using standard errors
confint.default(mylogit)

wald.test(b = coef(mylogit), Sigma = vcov(mylogit), Terms = 2:2)

l <- cbind(0,0,0,1,-1,0)
wald.test(b = coef(mylogit), Sigma = vcov(mylogit), L = l)

## odds ratios only
exp(coef(mylogit))

## odds ratios and 95% CI
exp(cbind(OR = coef(mylogit), confint(mylogit)))

newdata1 <- with(mydata,
                 data.frame(gre = mean(gre), gpa = mean(gpa), rank = factor(    1:4)))

## view data frame
newdata1

newdata1$rankP <- predict(mylogit, newdata = newdata1, type = "response")
newdata1

newdata2 <- with(mydata,
                 data.frame(gre = rep(seq(from = 200, to = 800, length.out =100), 4),
                            gpa = mean(gpa), rank = factor(rep(1:4, each = 100))))

newdata3 <- cbind(newdata2, predict(mylogit, newdata = newdata2, type="link", se=TRUE))
newdata3 <- within(newdata3, {
  PredictedProb <- plogis(fit)
  LL <- plogis(fit - (1.96 * se.fit))
  UL <- plogis(fit + (1.96 * se.fit))
})

## view first few rows of final dataset
head(newdata3)

ggplot(newdata3, aes(x = gre, y = PredictedProb)) +
  geom_ribbon(aes(ymin = LL, ymax = UL, fill = rank), alpha = .2) +
  geom_line(aes(colour = rank), size=1)

with(mylogit, null.deviance - deviance)

with(mylogit, df.null - df.residual)

with(mylogit, pchisq(null.deviance - deviance, df.null - df.residual, lower.tail = FALSE))

logLik(mylogit)
