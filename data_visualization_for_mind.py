# -*- coding: utf8 -*-. #
import pymysql
import sys
import matplotlib.pyplot as plt
from datetime import timedelta
from matplotlib import font_manager, rc
from matplotlib import style

reload(sys)
sys.setdefaultencoding('utf-8')

####### 마음남기기에 대한 데이터 시각화

mindid_dictionary_mindcount={}
mindid_dictionary_diarycount={}

mindid_dictionary={}
mindid_dictionary1={}
mindid_dictionary2={}
mindid_dictionary3={}

# MySQL Connection 연결
conn = pymysql.connect(host='52.79.138.56', user='rnduser', password='hongik_gwh',
                       db='falling', charset='utf8')
curs = conn.cursor()
idcount=1
sql0="select userId from MindView;"
curs.execute(sql0)
row_mindid = curs.fetchall()
for i in row_mindid:
    mindid_dictionary[i[0]]=0
    mindid_dictionary1[i[0]]=0


    idcount=idcount+1

sql = "select U.userId as uuserId,U.age as uage,U.gender as ugender,U.fallingStartDate as ufallingstartdate,matchDate as matchdate,countmind,countdiary,TU.userId as tuserId,TU.age as tage,TU.gender as tgender,TU.fallingStartDate as tfallingstartdate,hintCheckStatus, foundCheckStatus,inviteCheck,CASE When U.age-TU.age>0 and U.age-TU.age<=5 Then '1' When U.age-TU.age<0 and U.age-TU.age>=-5 then '-1' When U.age-TU.age>5 and U.age-TU.age<=10 Then '2' When U.age-TU.age>10 then '3' When U.age-TU.age>=-10 and U.age-TU.age<-5 then '-2' When U.age-TU.age<-10 then '-3' When U.age-TU.age=0 Then '0' END as agegrade,CASE When TimestampDiff(minute,U.fallingStartDate,TU.fallingStartDate)<=10 and TimestampDiff(minute,U.fallingStartDate,TU.fallingStartDate)>0 Then '0' When TimestampDiff(minute,U.fallingStartDate,TU.fallingStartDate)>60 and TimestampDiff(minute,U.fallingStartDate,TU.fallingStartDate)<=1440 Then '1'ELSE '2' END as timegrade,U.gender-TU.gender as gendergrade from (select M.foundCheck foundCheckStatus, M.hintCheck hintCheckStatus, R.mainUserId mainUserId,R.matchDate, R.inviteCheck, R.relId relationId, R.targetUserId,COUNT(M.mindId) countmind ,M.message messages,R.matchCheck relMatchStatus,COUNT(D.diaryId) countdiary from (RelationView R LEFT OUTER JOIN MindView M ON R.relId=M.relId) LEFT OUTER JOIN DiaryView D ON R.relId=D.relId group by R.relId) as gbByMindCount JOIN UserView as U on gbByMindCount.mainUserId=U.userId JOIN UserView as TU ON TU.userId=gbByMindCount.targetUserId where U.age is not NULL;"
curs.execute(sql)
User_dictionary={}
mind_dictionary={}
count1=0
count2=0
count3=0
count4=0
count5=0
count6=0
count7=0
count8=0
count9=0
count10=0
count12=0
count22=0
count32=0
count42=0
count52=0
count62=0
count72=0
count82=0
count92=0
count102=0
count_couple=0
count_join=0
rows = curs.fetchall()

for row in rows:
    #count_client = count_client + 1
    try:
        iff= mindid_dictionary[row[0]]

    except:
        #count_nomessage=count_nomessage+1
        continue
    sql2 = str("select hintCheck as mhintcheck,foundDate as mcheckdate,savedDate as msavedate,message as mcontent from MindView where userId=%s;" %row[0])
    curs.execute(sql2)
    messages = curs.fetchall()
    if messages.__len__()==0:
        continue

    list1=[]
    list2=[]
    check1=0
    check2=0
    count_message1=0
    count_message2=0
    for message in messages:
        check1 = 0
        check2 = 0
        if row[4] != None: #커플성사후
            if row[4] < message[2]:
                check1 = 1
                count_message1 = count_message1 + 1

                d=message[2]-row[4]
                #print type(d)
                secs = d.total_seconds()
                hours = int(secs / 3600)
                minutes = int(secs / 60) % 60
                if minutes<30:
                    count1=count1+1
                else:
                     if hours==0:
                        count2=count2+1
                     elif hours==1:
                         count3=count3+1
                     elif hours==2:
                         count4=count4+1
                     elif hours<=24:
                         count5=count5+1
                     elif hours<=48:
                        count6=count6+1
                     elif hours<=72:
                         count7=count7+1
                     elif hours<=96:
                         count8=count8+1
                     elif hours<=120:
                         count9=count9+1
                     else:
                         count10 = count10 + 1
                list1.append(d)





        if row[10] != None: #상대방가입후
            if row[10] < message[2]:

               # print row[10]
                count_message2 = count_message2 + 1
                d = (message[2] - row[10])
                check2=1
                secs = d.total_seconds()
                hours = int(secs / 3600)
                minutes = int(secs / 60) % 60
                if minutes < 30:
                    count12 = count12 + 1
                else:
                    if hours == 0:
                        count22 = count22 + 1
                    elif hours >=1 and hours<=2:
                        count32 = count32 + 1
                    elif hours <= 3:
                        count42 = count42 + 1
                    elif hours <= 24:
                        count52 = count52 + 1
                    elif hours <= 48:
                        count62 = count62 + 1
                    elif hours <= 72:
                        count72 = count72+ 1
                    elif hours <= 96:
                        count82 = count82 + 1
                    elif hours <= 120:
                        count92 = count92+ 1
                    else:
                        count102=count102+1
                list2.append(d)
    if check1>0:
        mindid_dictionary2[row[0]] = [count_message1]
        mindid_dictionary2[row[0]].append(list1)
        #print mindid_dictionary2[row[0]]
        count_couple = count_couple + 1
    if check2>0 and check1==0:

        mindid_dictionary3[row[0]] = [count_message2]
        mindid_dictionary3[row[0]].append(list2)
        count_join = count_join + 1
       # print mindid_dictionary3[row[0]]
       # print mindid_dictionary3[row[0]][0][0]

#        print mindid_dictionary3[row[0]][0][0][0]

print count_couple
print len(mindid_dictionary2)
print count_join
print len(mindid_dictionary3)

"""days=['30m','1h','2h','3h','1d','2d','3d','4d','5d','>5']
x=[1,2,3,4,5,6,7,8,9,10]
data1=[count1,count2,count3,count4,count5,count6,count7,count8,count9,count10]
data2=[count12,count22,count32,count42,count52,count62,count72,count82,count92,count102]
plt.bar(x,data1,label='after couple',alpha=0.7,color='g')
plt.xlabel("day")
plt.bar(x,data2,label='after join',alpha=0.4,color='r')


plt.ylabel("count")
plt.legend()
plt.title("메세지 남긴 비율")
plt.xticks(x,days)
#plt.show()
plt.pie(data1, labels=days, shadow=False, startangle=90)
plt.show()"""

xx=[1,2,3,4,5,6]
counts=['1','2','3','4','5','after']
yy=[0,0,0,0,0,0]
for key, val in mindid_dictionary2.items():

    if val[0]==1:
       yy[0]=yy[0]+1
    elif val[0]==2:
        yy[1] = yy[1] + 1
    elif val[0]==3:
        yy[2] = yy[2] + 1
    elif val[0]==4:
        yy[3] = yy[3] + 1
    elif val[0]==5:
        yy[4] = yy[4] + 1
    else:
        yy[5]=yy[5]+1

yy2=[0,0,0,0,0,0]
for key, val in mindid_dictionary3.items():
    if val[0]==1:
       yy2[0]=yy2[0]+1
    elif val[0]==2:
        yy2[1] = yy2[1] + 1
    elif val[0]==3:
        yy2[2] = yy2[2] + 1
    elif val[0]==4:
        yy2[3] = yy2[3] + 1
    elif val[0]==5:
        yy2[4] = yy2[4] + 1
    else:
        yy2[5]=yy2[5]+1

plt.bar(xx,yy,label='after couple',alpha=0.7,color='g')
plt.xlabel("messages")
plt.bar(xx,yy2,label='after join',alpha=0.4,color='r')


plt.ylabel("count")
plt.legend()
plt.title("count analysis")
plt.xticks(xx,counts)
plt.show()

print yy
print yy2
"""
plt.pie(yy2, labels=counts, shadow=True, startangle=90)
plt.show()"""


