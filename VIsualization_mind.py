# -*- coding: utf8 -*-. #
import pymysql
import sys
import matplotlib.pyplot as plt
from datetime import timedelta
from matplotlib import font_manager, rc
from matplotlib import style

reload(sys)
sys.setdefaultencoding('utf-8')



mindid_dictionary_mindcount={}
mindid_dictionary_diarycount={}

mindid_dictionary={}
mindid_dictionary1={}
mindid_dictionary2={}
mindid_dictionary3={}
X=[]
Y=[]
X2=[]
Y2=[]
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
count1,count2,count3,count4,count5,count6,count7,count8,count9,count10,count12,count22,count32,count42,count52,count62,count72,count82,count92,count102=0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
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
                list1.append(hours)





        if row[10] != None: #상대방가입후
            if row[10] < message[2]:

               # print row[10]
                count_message2 = count_message2 + 1
                d = (message[2] - row[10])
                check2=1
                secs = d.total_seconds()
                hours = int(secs / 3600)
                minutes = int(secs / 60) % 60

                list2.append(hours)
    if check1>0:
        mindid_dictionary2[row[0]] = [count_message1]
        mindid_dictionary2[row[0]].append(list1)
        #print mindid_dictionary2[row[0]]
        Y.append(count_message1)
        sum=0
        for i in list1:
            sum=sum+i
        d=sum/list1.__len__()
        X.append(d)

        count_couple = count_couple + 1
        if count_message1>5:
            print row[0],count_message1
    if check2>0 :

        mindid_dictionary3[row[0]] = [count_message2]
        mindid_dictionary3[row[0]].append(list2)
        count_join = count_join + 1
        Y2.append(count_message2)
        sum = 0
        for i in list2:
            sum = sum + i
        d = sum / list2.__len__()
        X2.append(d)
        #if count_message2>5:
           # print row[0],count_message2

       # print mindid_dictionary3[row[0]]
       # print mindid_dictionary3[row[0]][0][0]

#        print mindid_dictionary3[row[0]][0][0][0]
#plt.scatter(X2,Y2,label='dot_graph',color='r',alpha=0.3,marker='o')
#plt.show()
print count_couple
print count_join


