#与mysql数据库连接

import pymysql
# from flask_login._compat import unicode

pymysql.install_as_MySQLdb()
# from run import login_manager
from flask_login import UserMixin,AnonymousUserMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, CHAR, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,String
from sqlalchemy.orm import sessionmaker, relationship, backref
# from DB.operate import se


Base = declarative_base()

engine = create_engine('mysql+mysqldb://root:869999@localhost:3306/TestSystem?charset=utf8', echo=True)


Session = sessionmaker(bind=engine)
session = Session()


#对应数据库中Admin表
class Admin(UserMixin,Base):
    __tablename__ = 'Admin'

    name = Column(String, primary_key=True)
    password = Column(String)

    def __init__(self, name, password):
        self.name = name
        self.password = password


    def __repr__(self):
        return "<Admin(name='%s', password='%s')>" % (
                  self.name, self.password)

#对应数据库中User表
class User(Base):
    __tablename__ = 'User'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    Email = Column(String, nullable=True)
    sex = Column(CHAR, nullable=False,default='0')
    tel = Column(String,nullable=False)

    def __repr__(self):
        return "<User(id='%s', name='%s', password='%s', Email='%s', sex='%s', tel='%s')>" % (
                self.id, self.name, self.password, self.Email, self.sex, self.tel)

    def __init__(self, id, name, password, Email, sex, tel):
        self.id = id
        self.password = password
        self.name = name
        self.Email = Email
        self.sex = sex
        self.tel = tel

    def add(self):
        try:
            session.add(self)
            session.commit()
            return self.id
        except Exception as e:
            session.rollback()
            return e
        finally:
            return 0

    def isExisted(self):
        temUser = session.query(User).filter_by(id=self.id,password=self.password).first()
        if temUser is None:
            return 0
        else:
            return 1

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)  # python 3



#对应数据库中TestRecord表
class TestRecord(Base):
    __tablename__ = 'TestRecord'

    TestNum = Column(Integer, primary_key=True, autoincrement=True)
    achieveMent = Column(String, nullable=False)
    startTime = Column(TIMESTAMP, nullable=True)
    endTime = Column(TIMESTAMP, nullable=True)
    testCategory = Column(String, nullable=True)

    def __init__(self, TestNum, achieveMent, startTime, testCategory, endTime):
        self.TestNum = TestNum
        self.achieveMent = achieveMent
        self.startTime = startTime
        self.endTime = endTime
        self.testCategory = testCategory


    def __repr__(self):
        return "<TestRecord(TestNum='%d', achieveMent='%s')>" % (
                self.TestNum, self.achieveMent)

# 对应数据库中OneChooseItem表
class OneChooseItem(Base):
    __tablename__ = 'OneChooseItem'

    titleNo = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    chooseA = Column(String, nullable=False)
    chooseB = Column(String, nullable=False)
    chooseC = Column(String, nullable=False)
    chooseD = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    category = Column(String)


    def __init__(self, titleNo, content, chooseA,chooseB,chooseC,chooseD, answer,category):
        self.titleNo = titleNo
        self.content = content
        self.answer = answer
        self.chooseA = chooseA
        self.chooseB = chooseB
        self.chooseC = chooseC
        self.chooseD = chooseD
        self.category = category



    def add(self):
        try:
            session.add(self)
            session.commit()
            return self.titleNo
        except Exception as e:
            session.rollback()
            return e
        finally:
            return 0

    def delete(self):
        try:
            session.delete(self)
            session.commit()
            return self.titleNo
        except Exception as e:
            session.rollback()
            return e
        finally:
            return 0


    def __repr__(self):
        return "<oneChooseItem(titleNo='%d', content='%s', chooseA='%s', chooseB='%s',chooseC='%s',chooseD='%s',answer='%s', category='%s')>" % (
                self.titleNo, self.content, self.chooseA, self.chooseB,self.chooseC,self.chooseD, self.answer, self.category)


# 对应数据库中ManyChooseItem表
class ManyChooseItem(Base):
    __tablename__ = 'ManyChooseItem'

    titleNo = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    chooseA = Column(String, nullable=False)
    chooseB = Column(String, nullable=False)
    chooseC = Column(String, nullable=False)
    chooseD = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    category = Column(String)


    def __init__(self, titleNo, content, chooseA,chooseB,chooseC,chooseD, answer, category):
        self.titleNo = titleNo
        self.content = content
        self.answer = answer
        self.chooseA = chooseA
        self.chooseB = chooseB
        self.chooseC = chooseC
        self.chooseD = chooseD
        self.category = category


    def __repr__(self):
        return "<manyChooseItem(titleNo='%d', content='%s', chooseA='%s', chooseB='%s',chooseC='%s',chooseD='%s',answer='%s', category='%s')>" % (
                self.titleNo, self.content, self.chooseA, self.chooseB,self.chooseC,self.chooseD, self.answer, self.category)


    def add(self):
        try:
            session.add(self)
            session.commit()
            return self.titleNo
        except Exception as e:
            session.rollback()
            return e
        finally:
            return 0

    def delete(self):
        try:
            session.delete(self)
            session.commit()
            return self.titleNo
        except Exception as e:
            session.rollback()
            return e
        finally:
            return 0


# 对应数据库中true-flaseItem表
class turefalseItem(Base):
    __tablename__ = 'true-falseItem'

    content = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    titleNo = Column(Integer, primary_key=True)
    category = Column(String)

    def __repr__(self):
        return "<judgeItem(content='%s', titleNo='%s', answer='%s', category='%s')>" % (
            self.content, self.titleNo, self.answer, self.category)

    def __init__(self, titleNo, content, answer, category):
        self.titleNo = titleNo
        self.content = content
        self.answer = answer
        self.category = category

    def add(self):
        try:
            session.add(self)
            session.commit()
            return self.titleNo
        except Exception as e:
            session.rollback()
            return e
        finally:
            return 0

    def delete(self):
        try:
            session.delete(self)
            session.commit()
            return self.titleNo
        except Exception as e:
            session.rollback()
            return e
        finally:
            return 0

# 对应数据库中Search表
class Search(Base):
    __tablename__ = 'Search'

    num = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Integer, nullable=True)
    id = Column(String, ForeignKey('User.id', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)
    TestNum = Column(Integer, ForeignKey('TestRecord.TestNum', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)

    ids = relationship("User", backref=backref('Search', order_by=id))

    def __repr__(self):
        return "<Search(num='%s', id='%s', TestNum='%s')>" % (
            self.num, self.id, self.TestNum)

    def __init__(self, num, id, TestNum, score):
        self.num = num
        self.id = id
        self.TestNum = TestNum
        self.score = score


# 对应数据库中one-chooseOperate表
class oneChooseOperate(Base):
    __tablename__ = 'one-chooseOperate'

    drawnum = Column(Integer, primary_key=True, autoincrement=True)
    isCorrect = Column(String, nullable=True)
    titleNo_1 = Column(Integer, ForeignKey('OneChooseItem.titleNo', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)
    TestNum_1 = Column(Integer, ForeignKey('TestRecord.TestNum', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)

    def __repr__(self):
        return "<oneChooseOperate(isCorrect='%s')>" % (
            self.isCorrect)

    def __init__(self, drawnum, isCorrect, titleNo_1, TestNum_1):
        self.drawnum = drawnum
        self.isCorrect = isCorrect
        self.titleNo_1 = titleNo_1
        self.TestNum_1 = TestNum_1


# 对应数据库中many-chooseOperate表
class manyChooseOperate(Base):
    __tablename__ = 'many-chooseOperate'

    drawnum = Column(Integer, primary_key=True, autoincrement=True)
    isCorrect = Column(String, nullable=True)
    titleNo_2 = Column(Integer, ForeignKey('ManyChooseItem.titleNo', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)
    TestNum_2 = Column(Integer, ForeignKey('TestRecord.TestNum', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)

    def __repr__(self):
        return "<manyChooseOperate(isCorrect='%s')>" % (
            self.isCorrect)

    def __init__(self, drawnum, isCorrect, titleNo_2, TestNum_2):
        self.drawnum = drawnum
        self.isCorrect = isCorrect
        self.titleNo_2 = titleNo_2
        self.TestNum_2 = TestNum_2


# 对应数据库中judgeOperate表
class judgeOperate(Base):
    __tablename__ = 'judgeOperate'

    drawnum= Column(Integer, primary_key=True, autoincrement=True)
    isCorrect = Column(String, nullable=True)
    titleNo_3 = Column(Integer, ForeignKey('true-falseItem.titleNo', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)
    TestNum_3 = Column(Integer, ForeignKey('TestRecord.TestNum', ondelete='RESTRICT', onupdate='RESTRICT'), nullable=False)

    def __repr__(self):
        return "<judgeOperate(isCorrect='%s', drawnum ='%s')>" % (
            self.isCorrect, self.drawnum)

    def __init__(self, drawnum, isCorrect, titleNo_3, TestNum_3):
        self.drawnum = drawnum
        self.isCorrect = isCorrect
        self.titleNo_3 = titleNo_3
        self.TestNum_3 = TestNum_3

