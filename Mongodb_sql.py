import pymongo
# -*- coding: utf8 -*-. #
import pymysql
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

connection = pymongo.MongoClient("mongodb://rnduser:hongik_gwh@52.79.138.56:27017/fallingSNS")

conn = pymysql.connect(host='52.79.138.56', user='rnduser', password='hongik_gwh',
                       db='falling', charset='utf8')
curs = conn.cursor()
file = open("result_mongodb", "w")
db = connection['fallingSNS']
collection = db['contents']
docs = collection.find({})
mindid_dictionary = {}
sql0 = "select userId from MindView;"
curs.execute(sql0)
row_mindid = curs.fetchall()
for i in row_mindid:
    mindid_dictionary[i[0]] = 0
for i in docs:
    # print i
    mongoid = i['userId']
    sql = (
    "select U.userId as uuserId,U.age as uage,U.gender as ugender,U.fallingStartDate as ufallingstartdate,matchDate as matchdate,countmind,countdiary,TU.userId as tuserId,TU.age as tage,TU.gender as tgender,TU.fallingStartDate as tfallingstartdate,hintCheckStatus, foundCheckStatus,inviteCheck,CASE When U.age-TU.age>0 and U.age-TU.age<=5 Then '1' When U.age-TU.age<0 and U.age-TU.age>=-5 then '-1' When U.age-TU.age>5 and U.age-TU.age<=10 Then '2' When U.age-TU.age>10 then '3' When U.age-TU.age>=-10 and U.age-TU.age<-5 then '-2' When U.age-TU.age<-10 then '-3' When U.age-TU.age=0 Then '0' END as agegrade,CASE When TimestampDiff(minute,U.fallingStartDate,TU.fallingStartDate)<=10 and TimestampDiff(minute,U.fallingStartDate,TU.fallingStartDate)>0 Then '0' When TimestampDiff(minute,U.fallingStartDate,TU.fallingStartDate)>60 and TimestampDiff(minute,U.fallingStartDate,TU.fallingStartDate)<=1440 Then '1'ELSE '2' END as timegrade,U.gender-TU.gender as gendergrade from (select M.foundCheck foundCheckStatus, M.hintCheck hintCheckStatus, R.mainUserId mainUserId,R.matchDate, R.inviteCheck, R.relId relationId, R.targetUserId,COUNT(M.mindId) countmind ,M.message messages,R.matchCheck relMatchStatus,COUNT(D.diaryId) countdiary from (RelationView R LEFT OUTER JOIN MindView M ON R.relId=M.relId) LEFT OUTER JOIN DiaryView D ON R.relId=D.relId group by R.relId) as gbByMindCount JOIN UserView as U on gbByMindCount.mainUserId=U.userId JOIN UserView as TU ON TU.userId=gbByMindCount.targetUserId where U.age is not NULL and U.userId=%s;" % mongoid)
    curs.execute(sql)
    rows = curs.fetchall()
    sentence = "".join([str(a) + "," for a in rows])
    s=i['content'].replace('\n',' ')
    sentence=sentence+str(s)
    sentence=sentence+str(","+str(i['likes']['likeCount'])+',')

    try:
        iff = mindid_dictionary[rows[0]]
    except:
        sentence = sentence + '\n'
        sentence = sentence.replace(",\n", '\n')
        file.write(sentence)
        continue

