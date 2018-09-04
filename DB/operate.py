import pymysql
pymysql.install_as_MySQLdb()
import sqlalchemy
from time import strftime, localtime, time
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from flask_sqlalchemy import BaseQuery
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,String
from sqlalchemy.orm import sessionmaker, relationship, backref
from DB.orm import User,Admin,OneChooseItem, ManyChooseItem,turefalseItem, TestRecord, Search,manyChooseOperate,oneChooseOperate,judgeOperate
import random

engine = create_engine('mysql+mysqldb://root:869999@localhost:3306/TestSystem?charset=utf8', echo=True)


# ed_admin = Admin(name='ssw', password='12345')
# print(ed_admin)
class se():
    Session = sessionmaker(bind=engine)
    session = Session()

#
# print(session.query(Admin).all())
# #查询表中所有元素
#
# for row in session.query(Admin).order_by(Admin.name):
#     print(row)
# #session.add(ed_admin)
# #插入语句
# our_user = session.query(Admin).filter_by(name='ssw')
# #select * from Admin where name = "ssw"

# user = User(id='daafsx',
#                     password='123321',
#                     name='xiaocui',
#                     Email='597317165@qq.com',
#                     sex='0',
#                     tel=12432131)
# user.add()

#
# print(se.session.query(User).all())
# user = User(id='xiaowang', password='1234', name='', Email='', sex='0', tel=0)
#
# uInfo = se.session.query(User).filter(User.id=='xiaowang').first()
# print(uInfo.id)

# query = BaseQuery([Provider, email_subq], se.session())


# insOneChoose = OneChooseItem(titleNo=100001, content='下列叙述中正确的是',
#                              choose='A、算法就是程序 B、设计算法时只需要考虑数据结构的设计 C、设计算法时只需要考虑结果的可靠性 D、以上三种说法都不对',
#                              answer='D', num=2)
#
# x=se.session.query(ManyChooseItem).filter(ManyChooseItem.titleNo==200020).one()
#
# se.session.delete(x)
# se.session.commit()
# print(x)

# print(1)
# print(user.isExisted())

# upOneChoose = se.session.query(OneChooseItem).filter(OneChooseItem.titleNo == 100013).first()
# upOneChoose.answer = 'B'
# se.session.commit()

# upManyChoose = se.session.query(ManyChooseItem).filter(ManyChooseItem.titleNo == 200001).first()
# upManyChoose.answer = 'A、C'
# se.session.commit()
# print(upManyChoose)
# i=0
# pageSe = []
# oneNum = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
# manyNum = [21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
# judgeNum = [41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60]
# while i <= 60:
#     pageSe.append(i)
#     i = i + 1
#
# randOneTitle = se.session.query(OneChooseItem).order_by(func.rand()).limit(20).all()
# randManyTitle = se.session.query(ManyChooseItem).order_by(func.rand()).limit(20).all()
# randJudgeTitle = se.session.query(turefalseItem).order_by(func.rand()).limit(20).all()
#
# #
#
# a = []
#
# a.extend(randOneTitle)
# a.extend(randManyTitle)
# a.extend(randJudgeTitle)
#
# for i in a:
#     print(i.titleNo)

# for j in randOneTitle:
#     print(j.titleNo)
#
# print('*********************************')
#
# for j in pageSe:
#     if j in oneNum:
#         print(randOneTitle[j - 1].titleNo)
#     if j in manyNum:
#         print(randManyTitle[j - 21].titleNo)
#     if j in judgeNum:
#         print(randJudgeTitle[j - 41].titleNo)

# randOneTitle = se.session.query(OneChooseItem).order_by(func.rand()).limit(20).all()
# print(randOneTitle)
# str1 = ''
# i = 0
# while (i < 60):
#     str1 = str1 + str(a[i].titleNo) + ','
#     if i == 59:
#         str1 = str1 + str(a[i].titleNo)
#     i = i + 1
#
# print(str1)



# b = {}
# b[a[1].titleNo] = 'A'
# i = 1
# for key, value in b.items():
#     print(str(key) + ':' + value)
# print(b[a[1].titleNo])
#
# pageNum = se.session.query(func.count().label('count')).filter(Search.TestNum==TestRecord.TestNum).filter(Search.id==User.id).first()
# print(pageNum.count)

# searchResult = se.session.query(Search.num, User.id, TestRecord.achieveMent, TestRecord.startTime, TestRecord.endTime, Search.TestNum, Search.score).filter(TestRecord.TestNum==Search.TestNum).filter(Search.id==User.id).filter(User.id=="xiaocui").all()
# for result in searchResult:
#     print(result[0])
# oneInfo = se.session.query(TestRecord.TestNum, OneChooseItem.titleNo, oneChooseOperate.isCorrect).filter(TestRecord.TestNum == oneChooseOperate.TestNum_1).filter(oneChooseOperate.titleNo_1 == OneChooseItem.titleNo).subquery()
# print(oneInfo)
# manyInfo = se.session.query(TestRecord.TestNum, ManyChooseItem.titleNo, manyChooseOperate.isCorrect).filter(TestRecord.TestNum == manyChooseOperate.TestNum_2).filter(manyChooseOperate.titleNo_2 == ManyChooseItem.titleNo).subquery()
# print(manyInfo)
# judgeInfo = se.session.query(TestRecord.TestNum, turefalseItem.titleNo, judgeOperate.isCorrect).filter(TestRecord.TestNum == judgeOperate.TestNum_3).filter(judgeOperate.titleNo_3 == turefalseItem.titleNo).subquery()
# print(judgeInfo)
# searchResult = se.session.query(TestRecord.TestNum, User.id, TestRecord.startTime, OneChooseItem.titleNo, oneInfo.oneChooseOperate.isCorrect,
#                                 manyInfo.ManyChooseItem.titleNo,manyChooseOperate.isCorrect, judgeInfo.turefalseItem.titleNo,
#                                 judgeInfo.judgeOperate.isCorrect).filter(TestRecord.TestNum == Search.TestNum).filter(
#     Search.id == User.id).filter(oneInfo.TestRecord.TestNum == TestRecord.TestNum).filter(manyInfo.TestRecord.TestNum == TestRecord.TestNum).filter(
#     judgeInfo.TestRecord.TestNum == TestRecord.TestNum).all()
#
# totalNum = se.session.query(func.count('*').label('count')).filter(Search.TestNum == TestRecord.TestNum).filter(Search.id == User.id).filter(TestRecord.TestNum == oneChooseOperate.TestNum_1).filter(TestRecord.TestNum == manyChooseOperate.TestNum_2).filter(TestRecord.TestNum == judgeOperate.TestNum_3).filter(oneChooseOperate.titleNo_1 == OneChooseItem.titleNo).filter(manyChooseOperate.titleNo_2 == ManyChooseItem.titleNo).filter(judgeOperate.titleNo_3 == turefalseItem.titleNo).scalar()
#
# print(searchResult)
# print(totalNum)
# sql = "select TestRecord.TestNum,User.id, TestRecord.startTime, oneInfo.oneNum, manyInfo.manyNum, judgeInfo.judgeNum from " \
#       "(select TestRecord.TestNum as oneNum ,OneChooseItem.titleNo as oneTitle, oneChooseOperate.isCorrect as oneCorrect from TestRecord, one-chooseOperate, OneChooseItem where TestRecord.TestNum == one-chooseOperate.TestNum_1 and OneChooseItem.titleNo == one-chooseOperate.titleNo_1) " \
#       "oneInfo, (select TestRecord.TestNum as manyNum, OneChooseItem.titleNo as manyTitle, one-chooseOperate.isCorrect as manyCorret from TestRecord, many-chooseOperate, ManyChooseItem where TestRecord.TestNum == many-chooseOperate.TestNum_2 and ManyChooseItem == many-chooseOperate.titleNo_2) " \
#       "manyInfo, " \
#       "(select TestRecord.TestNum as judgeNum ,true-falseItem.titleNo as judgeTitle, judgeOperate.isCorrect as judgeCorret from TestRecord, judgeOperate, true-falseItem where TestRecord.TestNum == juageOperate.TestNum_3 and true-falseItem.titleNo == judgeOperate.titleNo_3)judgeInfo," \
#       "User, TestRecord, Search where User.id == Search.id and TestRecord.TestNum == Search.TestNum and oneInfo.oneNum == TestRecord.TestNum and manyInfo.manyNum == TestRecord.TestNum and TestRecord.TestNum == judgeInfo.juageNum"
# se.session.execute(sql)
#
# oneInfo = se.session.query(TestRecord.TestNum , User.id, OneChooseItem.titleNo, oneChooseOperate.isCorrect).filter(TestRecord.TestNum == Search.TestNum).filter(User.id == Search.id).filter(TestRecord.TestNum == oneChooseOperate.TestNum_1).filter(oneChooseOperate.titleNo_1 == OneChooseItem.titleNo).all()
# print(oneInfo)
# totalNum1 = se.session.query(func.count('*').label('count')).filter(Search.TestNum == TestRecord.TestNum).filter(Search.id == User.id).filter(TestRecord.TestNum == oneChooseOperate.TestNum_1).filter(oneChooseOperate.titleNo_1 == OneChooseItem.titleNo).scalar()
# print(totalNum1)
# # manyInfo = se.session.query(TestRecord.TestNum , User.id, ManyChooseItem.titleNo, manyChooseOperate.isCorrect).filter(TestRecord.TestNum == Search.TestNum).filter(User.id == Search.id).filter(TestRecord.TestNum == manyChooseOperate.TestNum_2).filter(manyChooseOperate.titleNo_2 == ManyChooseItem.titleNo).all()
# # print(manyInfo)
# totalNum2 = se.session.query(func.count('*').label('count')).filter(Search.TestNum == TestRecord.TestNum).filter(Search.id == User.id).filter(TestRecord.TestNum == manyChooseOperate.TestNum_2).filter(manyChooseOperate.titleNo_2 == ManyChooseItem.titleNo).scalar()
# print(totalNum2)
# # judgeInfo = se.session.query(TestRecord.TestNum , User.id, turefalseItem.titleNo, judgeOperate.isCorrect).filter(TestRecord.TestNum == Search.TestNum).filter(User.id == Search.id).filter(TestRecord.TestNum == judgeOperate.TestNum_3).filter(judgeOperate.titleNo_3 == turefalseItem.titleNo).all()
# # print(judgeInfo)
# totalNum3 = se.session.query(func.count('*').label('count')).filter(Search.TestNum == TestRecord.TestNum).filter(Search.id == User.id).filter(TestRecord.TestNum == judgeOperate.TestNum_3).filter(judgeOperate.titleNo_3 == turefalseItem.titleNo).scalar()
# print(totalNum3)


# categorySe = []
#
#
#
# oneChooseCategory = se.session.query(OneChooseItem.category).all()
#
# for oneCategorys in oneChooseCategory:
#     for oneCategory in oneCategorys:
#         if oneCategory not in categorySe and oneCategory != None:
#             categorySe.append(oneCategory)
#
#
#
#
# manyChooseCategory = se.session.query(ManyChooseItem.category).all()
#
# for manyCategorys in manyChooseCategory:
#     for manyCategory in manyCategorys:
#         if manyCategory not in categorySe and manyCategory != None:
#             categorySe.append(manyCategory)
#
#
#
# judgeCategory = se.session.query(turefalseItem.category).all()
#
# for jCategorys in judgeCategory:
#     for jCategory in jCategorys:
#         if jCategory not in categorySe and jCategory != None:
#             categorySe.append(jCategory)
#
#
#
#
# i = 0
#
# removeCateSe = []
#
# while i < len(categorySe):
#     print(i)
#     oneCateNum = se.session.query(OneChooseItem).filter(OneChooseItem.category == categorySe[i]).count()
#     manyCateNum = se.session.query(ManyChooseItem).filter(ManyChooseItem.category == categorySe[i]).count()
#     jCateNum = se.session.query(turefalseItem).filter(turefalseItem.category == categorySe[i]).count()
#     a = oneCateNum+manyCateNum+jCateNum
#     print(a)
#     if a < 10:
#         removeCateSe.append(categorySe[i])
#     else:
#         if categorySe[i] == '':
#             removeCateSe.append(categorySe[i])
#     i = i + 1
#
#
# for rcs in removeCateSe:
#     if rcs in categorySe:
#         categorySe.remove(rcs)
#
# print(categorySe)

# titleSe = []
# randOneTitle = se.session.query(OneChooseItem).filter(OneChooseItem.category == '微机原理').all()
# randManyTitle = se.session.query(ManyChooseItem).filter(ManyChooseItem.category == '微机原理').all()
# randJudgeTitle = se.session.query(turefalseItem).filter(turefalseItem.category == '微机原理').all()
#
# titleSe.extend(randOneTitle)
# titleSe.extend(randManyTitle)
# titleSe.extend(randJudgeTitle)
#
# print(titleSe)

