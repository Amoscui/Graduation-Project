from flask import render_template, flash, g
from flask import redirect ,url_for
from flask import request
from sqlalchemy import func

from web.forms import LoginForm,RegistrationForm, ForgetPasswordForm,AdminLoginForm, MainForm, UserInfo, AdminMainForm, \
    OneChooseTitle, ManyChooseTitle, JudgeTitle, ManagerAdmin, ManagerUser, BeginTestForm, OneChooseResult, ManyChooseResult, JudgeResult, BeginSpecialTestForm

from time import  localtime, time
from flask_login import login_user, logout_user, current_user

from DB.operate import se
from DB.orm import Admin, User, OneChooseItem, ManyChooseItem, turefalseItem, TestRecord, oneChooseOperate, manyChooseOperate, judgeOperate, Search
from . import webapp


@webapp.route('/admin', methods=['GET', 'POST'])
def adminLogin():
    adminloginForm = AdminLoginForm(request.form)
    if request.method == 'POST':
        baseAdmin = se.session.query(Admin).filter(Admin.name == adminloginForm.adminname.data).first()
        basePass = se.session.query(Admin).filter(Admin.name == adminloginForm.adminname.data).filter(
            Admin.password == adminloginForm.password.data).first()

        # user = User(loginForm.username.data, loginForm.password.data, ' ', ' ', '0', 0)
        # print(user.isExisted())
        # user = User(id=loginForm.username.data, password=loginForm.password.data, name='', Email='', sex='0', tel=0)
        # print(user.isExisted())

        if baseAdmin is not None and basePass is not None:
            return redirect(url_for('web.adminMain'), code=302)
        elif basePass is None and baseAdmin is not None:
            # 密码错误
            redirect(url_for('web.adminLogin'))
            flash('密码错误，请重新输入')
        elif baseAdmin is None:
            # 账号不存在
            redirect(url_for('web.adminLogin'))
            flash('账号不存在')

    return render_template('adminLogin.html', form=adminloginForm)


@webapp.route('/', methods=['GET','POST'])
def userLogin():
    loginForm = LoginForm(request.form)


    if loginForm.validate_on_submit() and request.method=='POST':
        baseID = se.session.query(User).filter(User.id==loginForm.username.data).first()
        basePass = se.session.query(User).filter(User.id==loginForm.username.data).filter(
            User.password==loginForm.password.data).first()

        # user = User(loginForm.username.data, loginForm.password.data, ' ', ' ', '0', 0)
        # print(user.isExisted())
        # user = User(id=loginForm.username.data, password=loginForm.password.data, name='', Email='', sex='0', tel=0)
        # print(user.isExisted())


        if baseID is not None and basePass is not None:
            login_user(basePass)
            return redirect(url_for('web.main'), code=302)
        elif basePass is None and baseID is not None:
            # 密码错误
            redirect(url_for('web.userLogin'))
            flash('密码错误，请重新输入')
        elif baseID is None:
            # 账号不存在
            redirect(url_for('web.userLogin'))
            flash('账号不存在请注册')

    return render_template('userLogin.html', form=loginForm)


#记录当前用户
@webapp.before_request
def before_request():
    g.user = current_user


#用户退出
@webapp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.userLogin'))


@webapp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method=='POST':
        if form.account.data != "" and form.password.data != "" and form.uname.data != "" and form.email.data != "" and form.tel.data != "":
            user = User(id=form.account.data,
                    password=form.password.data,
                    name=form.uname.data,
                    Email=form.email.data,
                    sex=form.sex.data,
                    tel=form.tel.data)
            se.session.add(user)
            try:
                se.session.commit()
            except:
                se.session.rollback()
                flash("该数据无效，请重新注册")
            return redirect(url_for('web.userLogin'))
        else:
            flash('请输入全部信息')

    # print('out print')
    return render_template('register.html',title='注册', form=form)

# 全局变量用于忘记密码判断
a = 0

@webapp.route('/forgetPassword', methods=['GET', 'POST'])
def forgetPassword():
    form = ForgetPasswordForm(request.form)
    global a
    if request.method == 'POST':
        baseAcc = se.session.query(User).filter(User.id == form.account.data).first()
        if request.form["action"] == "确认":
            if baseAcc is None:
                flash("账号不存在")
                a = 0
            else:
                a = 1
                flash("账号存在")
        elif request.form["action"] == "确定":
            if a == 1:
                baseAcc.password = form.newPassword.data
                se.session.commit()
                return redirect(url_for('web.userLogin'))
            else:
                flash("请先输入修改密码的账号")
    return render_template('forgetPassword.html', title='修改密码', form = form)


@webapp.route('/main/searchScore/<int:page>', methods=['GET','POST'])
def searchScore(page):
    #查询当前用户所有记录的数据
    searchResult = se.session.query(Search.num, User.id, TestRecord.achieveMent, TestRecord.startTime, TestRecord.endTime, Search.TestNum, Search.score, TestRecord.testCategory).filter(TestRecord.TestNum==Search.TestNum).filter(Search.id==User.id).filter(User.id==g.user.id).slice(
                    (page - 1) * 10, page * 10)
    #总记录数
    totalNum = se.session.query(func.count('*').label('count')).filter(Search.TestNum == TestRecord.TestNum).filter(User.id==g.user.id).filter(Search.id == User.id).scalar()
    #页数
    pageNum = totalNum / 10 - 1
    if page == 0:
        page = 1
    if page == None:
        page = 1
    if page < 1:
        page = 1
    if page > pageNum:
        page = pageNum
    pageSe = []
    i = 1
    while i <= pageNum:
        pageSe.append(i)
        i = i + 1
    return render_template('searchScore.html', title='成绩查询', page = page, pageSe=pageSe, searchResult=searchResult)


# # 用于判断选择考试类型
classflag = 0
# 存取考试题目
titleSe = []
#存取开始时间
sTime= None
#存取考试答案
testAnswer = {}
#用于判断点击考试题型选择标识
testflag = 0
#用于判断具体的专项考试类型
testClass = 0
#用于判断是是否选择考试类型的标识
isChoose = 0

#专项训练的题目类别集合
categorySe = {}

#点击题目生成的符合考试的类型列表
accChoice = [[],[],[]]

categoryName = ""

choice = []

@webapp.route('/main', methods=['GET', 'POST'])
def main():
    # 用于判断选择考试类型
    global classflag
    global sTime
    global testflag
    global titleSe
    global testClass
    global isChoose
    global choice
    global categoryName

    form = MainForm(request.form)
    if request.method == "POST":

        if request.form["action"] == "计算机":
            classflag = 1
            return redirect(url_for('web.main'))


        if request.form["action"] == "单项选择题":
            isChoose = 1
            categorySe['单项选择题'] = []
            choice = []
            oneChooseCategory = se.session.query(OneChooseItem.category).all()

            for oneCategorys in oneChooseCategory:
                for oneCategory in oneCategorys:
                    if oneCategory not in choice and oneCategory != None:
                        choice.append(oneCategory)

            i = 0

            removeCateSe = []

            while i < len(choice):
                oneCateNum = se.session.query(OneChooseItem).filter(OneChooseItem.category == choice[i]).count()
                if oneCateNum < 20:
                    removeCateSe.append(choice[i])
                else:
                    if choice[i] == '':
                        removeCateSe.append(choice[i])
                i = i + 1

            for rcs in removeCateSe:
                if rcs in choice:
                    choice.remove(rcs)

            categorySe['单项选择题'] = choice
            accChoice[isChoose - 1] =choice

            return redirect(url_for('web.main'))


        if request.form["action"] == "多项选择题":
            isChoose = 2
            categorySe['多项选择题'] = []
            choice = []
            manyChooseCategory = se.session.query(ManyChooseItem.category).all()

            for manyCategorys in manyChooseCategory:
                for manyCategory in manyCategorys:
                    if manyCategory not in choice and manyCategory != None:
                        choice.append(manyCategory)


            i = 0

            removeCateSe = []

            while i < len(choice):
                manyCateNum = se.session.query(ManyChooseItem).filter(ManyChooseItem.category == choice[i]).count()
                if manyCateNum < 20:
                    removeCateSe.append(choice[i])
                else:
                    if choice[i] == '':
                        removeCateSe.append(choice[i])
                i = i + 1

            for rcs in removeCateSe:
                if rcs in choice:
                    choice.remove(rcs)

            categorySe['多项选择题'] = choice
            accChoice[isChoose - 1] = choice

            return redirect(url_for('web.main'))


        if request.form["action"] == "判断题":
            isChoose = 3
            choice = []
            categorySe['判断题'] = []
            judgeCategory = se.session.query(turefalseItem.category).all()

            for jCategorys in judgeCategory:
                for jCategory in jCategorys:
                    if jCategory not in choice and jCategory != None:
                        choice.append(jCategory)


            i = 0

            removeCateSe = []

            while i < len(choice):
                jCateNum = se.session.query(turefalseItem).filter(turefalseItem.category == choice[i]).count()
                if jCateNum < 20:
                    removeCateSe.append(choice[i])
                else:
                    if choice[i] == '':
                        removeCateSe.append(choice[i])
                i = i + 1


            for rcs in removeCateSe:
                if rcs in choice:
                    choice.remove(rcs)

            categorySe['判断题'] = choice
            accChoice[isChoose - 1] = choice

            return redirect(url_for('web.main'))

        print(accChoice)

        a = 0
        while a < len(accChoice[isChoose - 1]):
            if request.form["action"] == accChoice[isChoose - 1][a]:
                testClass = a + 1
                categoryName = accChoice[isChoose - 1][a]
            a = a + 1
        print(categoryName)


        if request.form["action"] == "开始普通考试":
            if classflag == 0 :
                flash("请选择考试科目或类型")
                return redirect(url_for('web.main'))
            else:
                classflag = 1
                page = 1
                testflag = 0

                # 存取开始时间
                startTime = localtime(time())
                sTime = startTime

                # 随机取出题号
                randOneTitle = se.session.query(OneChooseItem).order_by(func.rand()).limit(20).all()
                randManyTitle = se.session.query(ManyChooseItem).order_by(func.rand()).limit(20).all()
                randJudgeTitle = se.session.query(turefalseItem).order_by(func.rand()).limit(20).all()

                titleSe.extend(randOneTitle)
                titleSe.extend(randManyTitle)
                titleSe.extend(randJudgeTitle)

                # print(titleSe)

                # 考试题目编号
                testTitle = ''
                i = 0
                while (i < 60):
                    if i == 59:
                        testTitle = testTitle + str(titleSe[i].titleNo)
                    else:
                        testTitle = testTitle + str(titleSe[i].titleNo) + ','
                    i = i + 1

                print(testTitle)

                # 添加考试记录
                addRecord = TestRecord(TestNum=0, achieveMent=testTitle, startTime=startTime, endTime=startTime, testCategory='普通考试')
                se.session.add(addRecord)
                se.session.commit()

                i = 0
                while i < 60:
                    if i < 20 or i >= 40:
                        testAnswer[titleSe[i].titleNo] = ''
                    else:
                        testAnswer[titleSe[i].titleNo] = []
                    i = i + 1

            return redirect(url_for('web.beginTest', page=1))



        if request.form["action"] == "开始专项考试":
            if classflag == 0 or testClass == 0 or isChoose == 0:
                flash("请选择考试科目或专项考试类型")

                return redirect(url_for('web.main'))
            else:
                classflag = 1

                # 存取开始时间
                startTime = localtime(time())
                sTime = startTime


                if isChoose == 1:
                    titleSe = se.session.query(OneChooseItem).filter(OneChooseItem.category == categoryName).order_by(func.rand()).limit(20).all()
                if isChoose == 2:
                    titleSe = se.session.query(ManyChooseItem).filter(ManyChooseItem.category == categoryName).order_by(
                        func.rand()).limit(20).all()
                if isChoose == 3:
                    titleSe = se.session.query(turefalseItem).filter(turefalseItem.category == categoryName).order_by(
                        func.rand()).limit(20).all()

                print(titleSe)

                testTitle = ''
                i = 0
                while (i < 20):
                    if i == 19:
                        testTitle = testTitle + str(titleSe[i].titleNo)
                    else:
                        testTitle = testTitle + str(titleSe[i].titleNo) + ','
                    i = i + 1

                print(testTitle)

                #添加考试记录
                addRecord = TestRecord(TestNum=0, achieveMent=testTitle, startTime=startTime, endTime=startTime,
                                       testCategory='专项考试' + '-' + categoryName)
                se.session.add(addRecord)
                se.session.commit()

                i = 0
                while i < 20:
                    if isChoose == 1 or isChoose == 3:
                        testAnswer[titleSe[i].titleNo] = ''
                    else:
                        testAnswer[titleSe[i].titleNo] = []
                    i = i + 1


            return redirect(url_for('web.beginSpecialTest', page=1))



        if request.form["action"] == "成绩查询":
            return redirect(url_for('web.searchScore', page=1))

    return render_template('main.html', title='主界面', form=form, flag=classflag, time=time, categorySe=categorySe, isChoose=isChoose, choice=choice)


clinkANum = 0
clinkBNum = 0
clinkCNum = 0
clinkDNum = 0
clinkTrue = 0
clinkFalse = 0


@webapp.route('/main/beginTest/<int:page>', methods=['GET', 'POST'])
def beginTest(page):
    # i = 1
    # 判断是否点击按键
    global startTime
    global classflag
    global clinkANum
    global clinkBNum
    global clinkCNum
    global clinkDNum
    global clinkTrue
    global clinkFalse
    global testClass
    global titleSe
    pageNum = 60
    # 用户选择答案
    answer = ''

    if page == 0:
        page = 1
    if page == None:
        page = 1
    if page < 1:
        page = 1
    if page > pageNum:
        page = pageNum

    judgeNum = [41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]

    form = BeginTestForm(request.form)

    if request.method == "POST":
        if request.form["action"] == " 交卷 ":
            classflag = 0
            testClass = 0
            # 获取考试的记录号
            nowTest = se.session.query(TestRecord).filter(TestRecord.startTime == sTime).first()
            testRecord = nowTest.TestNum
            endTime = localtime(time())
            se.session.query(TestRecord).filter(TestRecord.startTime == sTime).update({TestRecord.endTime: endTime},
                                                                                      synchronize_session=False)
            se.session.commit()

            a = 0
            oneDrawnum = ''
            manyDrawnum = ''
            judgeDrawnum = ''
            oneCorrectnum = 0
            manyCorrectnum = 0
            judgeCorrectnum = 0

            isCorrectOne = ''
            isCorrectMany = ''
            isCorrectJudge = ''
            while a < 60:
                if a < 20:
                    oneDrawnum = titleSe[a].titleNo
                    if testAnswer[titleSe[a].titleNo] == titleSe[a].answer:
                        isCorrectOne = "正确"
                        # oneCorrectNo = str(titleSe[a].titleNo) + ',' + oneCorrectNo
                        oneCorrectnum = oneCorrectnum + 1
                    else:
                        isCorrectOne = "错误"
                    addOneOperate = oneChooseOperate(TestNum_1=testRecord, titleNo_1=oneDrawnum,
                                                     isCorrect=isCorrectOne, drawnum=0)
                    se.session.add(addOneOperate)
                    try:
                        se.session.commit()
                    except:
                        se.session.rollback()

                if a >= 20 and a < 40:
                    manyDrawnum = titleSe[a].titleNo  # + ',' + manyDrawnum
                    answerlist = titleSe[a].answer.split(',')
                    chAns = testAnswer[titleSe[a].titleNo]
                    # print(chAns)
                    # print(answerlist)
                    if len(chAns) == len(answerlist):
                        for chooseAnswer in chAns:
                            if chooseAnswer in answerlist:
                                index = answerlist.index(chooseAnswer)
                                answerlist.pop(index)
                    # print(answerlist)
                    if answerlist == []:
                        # manyCorrectNo = str(titleSe[a].titleNo) + ',' + manyCorrectNo
                        manyCorrectnum = manyCorrectnum + 1
                        isCorrectMany = "正确"
                    else:
                        isCorrectMany = "错误"
                    addManyOperate = manyChooseOperate(TestNum_2=testRecord, drawnum=0,
                                                       isCorrect=isCorrectMany, titleNo_2=manyDrawnum)
                    se.session.add(addManyOperate)
                    try:
                        se.session.commit()
                    except:
                        se.session.rollback()

                if a >= 40:
                    judgeDrawnum = titleSe[a].titleNo  # + ',' + judgeDrawnum
                    if testAnswer[titleSe[a].titleNo] == titleSe[a].answer:
                        isCorrectJudge = "正确"
                        judgeCorrectnum = judgeCorrectnum + 1
                    else:
                        isCorrectJudge = "错误"
                        # judgeCorrectNo = str(titleSe[a].titleNo) + ',' + judgeCorrectNo

                    addJudgeOperate = judgeOperate(TestNum_3=testRecord, drawnum=0, titleNo_3=judgeDrawnum,
                                                   isCorrect=isCorrectJudge)
                    se.session.add(addJudgeOperate)
                    try:
                        se.session.commit()
                    except:
                        se.session.rollback()

                a = a + 1

            # print('抽取单选题题号：' + oneDrawnum)
            # print('抽取多选题题号：' + manyDrawnum)
            # print('抽取判断题题号：' + judgeDrawnum)
            # print('单选题正确个数：' + str(oneCorrectnum))
            # print('多选题正确个数：' + str(manyCorrectnum))
            # print('判断题正确个数：' + str(judgeCorrectnum))
            # print('单选题正确题号: ' + oneCorrectNo)
            # print('多选题正确题号: ' + manyCorrectNo)
            # print('判断题正确题号: ' + judgeCorrectNo)
            # 总成绩
            totalscore = oneCorrectnum + manyCorrectnum * 3 + judgeCorrectnum
            addSearch = Search(num=0, TestNum=testRecord, id=g.user.id, score=totalscore)
            se.session.add(addSearch)
            try:
                se.session.commit()
            except:
                se.session.rollback()

            titleSe.clear()
            testAnswer.clear()
            return redirect(url_for('web.main'))

        if page < 21 and page >= 41:
            testAnswer[titleSe[page - 1].titleNo] = ''


        if request.form["action"] == "A":
            if page < 21:
                clinkANum = 1
                clinkBNum = 0
                clinkCNum = 0
                clinkDNum = 0
                testAnswer[titleSe[page - 1].titleNo] = 'A'
            else:
                clinkANum = clinkANum + 1
                if clinkANum % 2 != 0:
                    testAnswer.setdefault(titleSe[page - 1].titleNo, []).append('A')
                else:
                    testAnswer.setdefault(titleSe[page - 1].titleNo, []).remove('A')

            return redirect(url_for('web.beginTest', page=page))

        if request.form["action"] == "B":
            if page < 21:
                clinkANum = 0
                clinkBNum = 1
                clinkCNum = 0
                clinkDNum = 0
                testAnswer[titleSe[page - 1].titleNo] = 'B'
            else:
                clinkBNum = clinkBNum + 1
                if clinkBNum % 2 != 0:
                    testAnswer.setdefault(titleSe[page - 1].titleNo, []).append('B')
                else:
                    testAnswer.setdefault(titleSe[page - 1].titleNo, []).remove('B')
            return redirect(url_for('web.beginTest', page=page))

        if request.form["action"] == "C":
            if page < 21:
                clinkANum = 0
                clinkBNum = 0
                clinkCNum = 1
                clinkDNum = 0
                testAnswer[titleSe[page - 1].titleNo] = 'C'
            else:
                clinkCNum = clinkCNum + 1
                if clinkCNum % 2 != 0:
                    testAnswer.setdefault(titleSe[page - 1].titleNo, []).append('C')
                else:
                    testAnswer.setdefault(titleSe[page - 1].titleNo, []).remove('C')
            return redirect(url_for('web.beginTest', page=page))

        if request.form["action"] == "D":
            if page < 21:
                clinkANum = 0
                clinkBNum = 0
                clinkCNum = 0
                clinkDNum = 1
                testAnswer[titleSe[page - 1].titleNo] = 'D'
            else:
                clinkDNum = clinkDNum + 1

                if clinkDNum % 2 != 0:
                    testAnswer.setdefault(titleSe[page - 1].titleNo, []).append('D')
                else:
                    testAnswer.setdefault(titleSe[page - 1].titleNo, []).remove('D')
            return redirect(url_for('web.beginTest', page=page))

        if request.form["action"] == "True":
            if page >= 41:
                clinkTrue = 1
                clinkFalse = 0
                testAnswer[titleSe[page - 1].titleNo] = "True"
            return redirect(url_for('web.beginTest', page=page))

        if request.form["action"] == "False":
            if page >= 41:
                clinkTrue = 0
                clinkFalse = 1
                testAnswer[titleSe[page - 1].titleNo] = "False"
            return redirect(url_for('web.beginTest', page=page))

        if request.form["action"] == "上一题":
            page1 = page - 1
            if page1 < 21:
                if testAnswer[titleSe[page1 - 1].titleNo] == "A":
                    clinkANum = 1
                else:
                    clinkANum = 0
                if testAnswer[titleSe[page1 - 1].titleNo] == "B":
                    clinkBNum = 1
                else:
                    clinkBNum = 0
                if testAnswer[titleSe[page1 - 1].titleNo] == "C":
                    clinkCNum = 1
                else:
                    clinkCNum = 0
                if testAnswer[titleSe[page1 - 1].titleNo] == "D":
                    clinkDNum = 1
                else:
                    clinkDNum = 0
                if testAnswer[titleSe[page1 - 1].titleNo] == ' ':
                    clinkANum = 0
                    clinkBNum = 0
                    clinkCNum = 0
                    clinkDNum = 0
            if page1 >= 21 and page1 < 41:
                clinkANum = 0
                clinkBNum = 0
                clinkCNum = 0
                clinkDNum = 0
                for list in testAnswer[titleSe[page1 - 1].titleNo]:
                    if list == 'A':
                        clinkANum = 1
                        continue

                    elif list == 'B':
                        clinkBNum = 1
                        continue

                    elif list == 'C':
                        clinkCNum = 1
                        continue

                    elif list == 'D':
                        clinkDNum = 1
                        continue

            if page1 >= 41:
                if testAnswer[titleSe[page1 - 1].titleNo] == "True":
                    clinkTrue = 1
                else:
                    clinkTrue = 0
                if testAnswer[titleSe[page1 - 1].titleNo] == "False":
                    clinkFalse = 1
                else:
                    clinkFalse = 0
                if testAnswer[titleSe[page1 - 1].titleNo] == "":
                    clinkTrue = 0
                    clinkFalse = 0
            return redirect(url_for('web.beginTest', page=page1))

        if request.form["action"] == "下一题":
            page2 = page + 1
            if testAnswer[titleSe[page2 - 1].titleNo] == '' or testAnswer[titleSe[page2 - 1].titleNo] == []:
                clinkANum = 0
                clinkBNum = 0
                clinkCNum = 0
                clinkDNum = 0
                clinkTrue = 0
                clinkFalse = 0
            else:
                if page2 < 21:
                    if testAnswer[titleSe[page2 - 1].titleNo] == "A":
                        clinkANum = 1
                    else:
                        clinkANum = 0
                    if testAnswer[titleSe[page2 - 1].titleNo] == "B":
                        clinkBNum = 1
                    else:
                        clinkBNum = 0
                    if testAnswer[titleSe[page2 - 1].titleNo] == "C":
                        clinkCNum = 1
                    else:
                        clinkCNum = 0
                    if testAnswer[titleSe[page2 - 1].titleNo] == "D":
                        clinkDNum = 1
                    else:
                        clinkDNum = 0
                    if testAnswer[titleSe[page2 - 1].titleNo] == ' ':
                        clinkANum = 0
                        clinkBNum = 0
                        clinkCNum = 0
                        clinkDNum = 0
                if page2 >= 21 and page2 < 41:
                    clinkANum = 0
                    clinkBNum = 0
                    clinkCNum = 0
                    clinkDNum = 0
                    for list in testAnswer[titleSe[page2 - 1].titleNo]:
                        if list == 'A':
                            clinkANum = 1
                            continue

                        elif list == 'B':
                            clinkBNum = 1
                            continue

                        elif list == 'C':
                            clinkCNum = 1
                            continue

                        elif list == 'D':
                            clinkDNum = 1
                            continue

                if page2 >= 41:
                    if testAnswer[titleSe[page2 - 1].titleNo] == "True":
                        clinkTrue = 1
                    else:
                        clinkTrue = 0
                    if testAnswer[titleSe[page2 - 1].titleNo] == "False":
                        clinkFalse = 1
                    else:
                        clinkFalse = 0
                    if testAnswer[titleSe[page2 - 1].titleNo] == "":
                        clinkTrue = 0
                        clinkFalse = 0
            return redirect(url_for('web.beginTest', page=page2))

        if request.form["action"] == "首页":
            page = 1
            if testAnswer[titleSe[page - 1].titleNo] == "A":
                clinkANum = 1
            else:
                clinkANum = 0
            if testAnswer[titleSe[page - 1].titleNo] == "B":
                clinkBNum = 1
            else:
                clinkBNum = 0
            if testAnswer[titleSe[page - 1].titleNo] == "C":
                clinkCNum = 1
            else:
                clinkCNum = 0
            if testAnswer[titleSe[page - 1].titleNo] == "D":
                clinkDNum = 1
            else:
                clinkDNum = 0
            if testAnswer[titleSe[page - 1].titleNo] == ' ':
                clinkANum = 0
                clinkBNum = 0
                clinkCNum = 0
                clinkDNum = 0
            return redirect(url_for('web.beginTest', page=page))

        if request.form["action"] == "尾页":
            page = 60
            if testAnswer[titleSe[page - 1].titleNo] == "True":
                clinkTrue = 1
            else:
                clinkTrue = 0
            if testAnswer[titleSe[page - 1].titleNo] == "False":
                clinkFalse = 1
            else:
                clinkFalse = 0
            if testAnswer[titleSe[page - 1].titleNo] == "":
                    clinkTrue = 0
                    clinkFalse = 0
            return redirect(url_for('web.beginTest', page=page))

        if request.form["action"] == "跳转":
            if form.gotoPage.data < 1:
                flash('没有零及负数页哦！')
                return redirect(url_for('web.beginTest', page=page))
            elif form.gotoPage.data > 60:
                flash('最多有60页哦！')
                return redirect(url_for('web.beginTest', page=page))
            else:
                if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == '' or testAnswer[
                    titleSe[form.gotoPage.data - 1].titleNo] == []:
                    clinkANum = 0
                    clinkBNum = 0
                    clinkCNum = 0
                    clinkDNum = 0
                    clinkTrue = 0
                    clinkFalse = 0
                else:
                    if form.gotoPage.data < 21 and form.gotoPage.data >= 1:
                        if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == "A":
                            clinkANum = 1
                        else:
                            clinkANum = 0
                        if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == "B":
                            clinkBNum = 1
                        else:
                            clinkBNum = 0
                        if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == "C":
                            clinkCNum = 1
                        else:
                            clinkCNum = 0
                        if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == "D":
                            clinkDNum = 1
                        else:
                            clinkDNum = 0
                        if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == ' ':
                            clinkANum = 0
                            clinkBNum = 0
                            clinkCNum = 0
                            clinkDNum = 0
                    if form.gotoPage.data >= 21 and form.gotoPage.data < 41:
                        clinkANum = 0
                        clinkBNum = 0
                        clinkCNum = 0
                        clinkDNum = 0
                        for list in testAnswer[titleSe[form.gotoPage.data - 1].titleNo]:
                            if list == 'A':
                                clinkANum = 1
                                continue

                            elif list == 'B':
                                clinkBNum = 1
                                continue

                            elif list == 'C':
                                clinkCNum = 1
                                continue

                            elif list == 'D':
                                clinkDNum = 1
                                continue

                    if form.gotoPage.data >= 41 and form.gotoPage.data <= 60:
                        if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == "True":
                            clinkTrue = 1
                        else:
                            clinkTrue = 0
                        if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == "False":
                            clinkFalse = 1
                        else:
                            clinkFalse = 0
                        if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == "":
                            clinkTrue = 0
                            clinkFalse = 0

                return redirect(url_for('web.beginTest', page=form.gotoPage.data))

    return render_template('beginTest.html', title='普通考试', form=form, flag=classflag,
                           page=page, titleSe=titleSe, judgeNum=judgeNum, clinkANum=clinkANum, clinkBNum=clinkBNum,
                           clinkCNum=clinkCNum, clinkDNum=clinkDNum, answer=answer, clinkTrue=clinkTrue,
                           clinkFalse=clinkFalse)




@webapp.route('/main/beginSpecialTest/<int:page>', methods=['GET', 'POST'])
def beginSpecialTest(page):
    global startTime
    global classflag
    global clinkANum
    global clinkBNum
    global clinkCNum
    global clinkDNum
    global clinkTrue
    global clinkFalse
    global testClass
    global titleSe
    global testAnswer
    global isChoose
    pageNum = 20
    # 用户选择答案
    answer = ''

    if page == 0:
        page = 1
    if page == None:
        page = 1
    if page < 1:
        page = 1
    if page > pageNum:
        page = pageNum


    form = BeginSpecialTestForm(request.form)

    #isChoose = 1单选
    #isChoose = 2多选
    #isChoose = 3判断

    if request.method == "POST":

        if request.form["action"] == " 交卷 ":
            classflag = 0
            testClass = 0

            categoryName = ''
            # 获取考试的记录号
            nowTest = se.session.query(TestRecord).filter(TestRecord.startTime == sTime).first()
            testRecord = nowTest.TestNum
            endTime = localtime(time())
            se.session.query(TestRecord).filter(TestRecord.startTime == sTime).update({TestRecord.endTime: endTime},
                                                                                      synchronize_session=False)
            se.session.commit()

            a = 0
            oneDrawnum = ''
            manyDrawnum = ''
            judgeDrawnum = ''
            oneCorrectnum = 0
            manyCorrectnum = 0
            judgeCorrectnum = 0

            isCorrectOne = ""
            isCorrectMany = ""
            isCorrectJudge = ""
            while a < 20:
                if isChoose == 1:
                    oneDrawnum = titleSe[a].titleNo
                    if testAnswer[titleSe[a].titleNo] == titleSe[a].answer:
                        isCorrectOne = "正确"
                        # oneCorrectNo = str(titleSe[a].titleNo) + ',' + oneCorrectNo
                        oneCorrectnum = oneCorrectnum + 1
                        print(oneCorrectnum)
                    else:
                        isCorrectOne = "错误"
                    addOneOperate = oneChooseOperate(TestNum_1=testRecord, titleNo_1=oneDrawnum,
                                                     isCorrect=isCorrectOne, drawnum=0)
                    se.session.add(addOneOperate)
                    try:
                        se.session.commit()
                    except:
                        se.session.rollback()

                if isChoose == 2:
                    manyDrawnum = titleSe[a].titleNo  # + ',' + manyDrawnum
                    answerlist = titleSe[a].answer.split(',')
                    chAns = testAnswer[titleSe[a].titleNo]
                    # print(chAns)
                    # print(answerlist)
                    if len(chAns) == len(answerlist):
                        for chooseAnswer in chAns:
                            if chooseAnswer in answerlist:
                                index = answerlist.index(chooseAnswer)
                                answerlist.pop(index)
                    # print(answerlist)
                    if answerlist == []:
                        # manyCorrectNo = str(titleSe[a].titleNo) + ',' + manyCorrectNo
                        manyCorrectnum = manyCorrectnum + 1
                        isCorrectMany = "正确"
                    else:
                        isCorrectMany = "错误"
                    addManyOperate = manyChooseOperate(TestNum_2=testRecord, drawnum=0,
                                                       isCorrect=isCorrectMany, titleNo_2=manyDrawnum)
                    se.session.add(addManyOperate)
                    try:
                        se.session.commit()
                    except:
                        se.session.rollback()

                if isChoose == 3:
                    judgeDrawnum = titleSe[a].titleNo  # + ',' + judgeDrawnum
                    if testAnswer[titleSe[a].titleNo] == titleSe[a].answer:
                        isCorrectJudge = "正确"
                        judgeCorrectnum = judgeCorrectnum + 1
                    else:
                        isCorrectJudge = "错误"
                        # judgeCorrectNo = str(titleSe[a].titleNo) + ',' + judgeCorrectNo

                    addJudgeOperate = judgeOperate(TestNum_3=testRecord, drawnum=0, titleNo_3=judgeDrawnum,
                                                   isCorrect=isCorrectJudge)
                    se.session.add(addJudgeOperate)
                    try:
                        se.session.commit()
                    except:
                        se.session.rollback()

                a = a + 1

            # print('抽取单选题题号：' + oneDrawnum)
            # print('抽取多选题题号：' + manyDrawnum)
            # print('抽取判断题题号：' + judgeDrawnum)
            # print('单选题正确个数：' + str(oneCorrectnum))
            # print('多选题正确个数：' + str(manyCorrectnum))
            # print('判断题正确个数：' + str(judgeCorrectnum))
            # print('单选题正确题号: ' + oneCorrectNo)
            # print('多选题正确题号: ' + manyCorrectNo)
            # print('判断题正确题号: ' + judgeCorrectNo)
            # 总成绩


            totalscore = oneCorrectnum + manyCorrectnum  + judgeCorrectnum
            addSearch = Search(num=0, TestNum=testRecord, id=g.user.id, score=totalscore)
            se.session.add(addSearch)
            try:
                se.session.commit()
            except:
                se.session.rollback()

            titleSe.clear()
            testAnswer.clear()
            categoryName = ""
            isChoose = 0
            return redirect(url_for('web.main'))



        if request.form["action"] == "A":
            if isChoose == 1:
                clinkANum = 1
                clinkBNum = 0
                clinkCNum = 0
                clinkDNum = 0
                testAnswer[titleSe[page - 1].titleNo] = 'A'
            elif isChoose == 2:
                clinkANum = clinkANum + 1
                if clinkANum % 2 != 0:
                    testAnswer.setdefault(titleSe[page - 1].titleNo, []).append('A')
                else:
                    testAnswer.setdefault(titleSe[page - 1].titleNo, []).remove('A')

            return redirect(url_for('web.beginSpecialTest', page=page))

        if request.form["action"] == "B":
            if isChoose == 1:
                clinkANum = 0
                clinkBNum = 1
                clinkCNum = 0
                clinkDNum = 0
                testAnswer[titleSe[page - 1].titleNo] = 'B'
            elif isChoose == 2:
                clinkBNum = clinkBNum + 1
                if clinkBNum % 2 != 0:
                    testAnswer.setdefault(titleSe[page - 1].titleNo, []).append('B')
                else:
                    testAnswer.setdefault(titleSe[page - 1].titleNo, []).remove('B')
            return redirect(url_for('web.beginSpecialTest', page=page))

        if request.form["action"] == "C":
            if isChoose == 1:
                clinkANum = 0
                clinkBNum = 0
                clinkCNum = 1
                clinkDNum = 0
                testAnswer[titleSe[page - 1].titleNo] = 'C'
            elif isChoose == 2:
                clinkCNum = clinkCNum + 1
                if clinkCNum % 2 != 0:
                    testAnswer.setdefault(titleSe[page - 1].titleNo, []).append('C')
                else:
                    testAnswer.setdefault(titleSe[page - 1].titleNo, []).remove('C')
            return redirect(url_for('web.beginSpecialTest', page=page))

        if request.form["action"] == "D":
            if isChoose == 1:
                clinkANum = 0
                clinkBNum = 0
                clinkCNum = 0
                clinkDNum = 1
                testAnswer[titleSe[page - 1].titleNo] = 'D'
            elif isChoose == 2:
                clinkDNum = clinkDNum + 1

                if clinkDNum % 2 != 0:
                    testAnswer.setdefault(titleSe[page - 1].titleNo, []).append('D')
                else:
                    testAnswer.setdefault(titleSe[page - 1].titleNo, []).remove('D')
            return redirect(url_for('web.beginSpecialTest', page=page))

        if request.form["action"] == "True":
            if isChoose == 3:
                clinkTrue = 1
                clinkFalse = 0
                testAnswer[titleSe[page - 1].titleNo] = "True"
            return redirect(url_for('web.beginSpecialTest', page=page))

        if request.form["action"] == "False":
            if isChoose == 3:
                clinkTrue = 0
                clinkFalse = 1
                testAnswer[titleSe[page - 1].titleNo] = "False"
            return redirect(url_for('web.beginSpecialTest', page=page))

        if request.form["action"] == "上一题":
            page1 = page - 1
            if isChoose == 1:
                if testAnswer[titleSe[page1 - 1].titleNo] == "A":
                    clinkANum = 1
                else:
                    clinkANum = 0
                if testAnswer[titleSe[page1 - 1].titleNo] == "B":
                    clinkBNum = 1
                else:
                    clinkBNum = 0
                if testAnswer[titleSe[page1 - 1].titleNo] == "C":
                    clinkCNum = 1
                else:
                    clinkCNum = 0
                if testAnswer[titleSe[page1 - 1].titleNo] == "D":
                    clinkDNum = 1
                else:
                    clinkDNum = 0
                if testAnswer[titleSe[page1 - 1].titleNo] == ' ':
                    clinkANum = 0
                    clinkBNum = 0
                    clinkCNum = 0
                    clinkDNum = 0
            if isChoose == 2:
                clinkANum = 0
                clinkBNum = 0
                clinkCNum = 0
                clinkDNum = 0
                for list in testAnswer[titleSe[page1 - 1].titleNo]:
                    if list == 'A':
                        clinkANum = 1
                        continue

                    elif list == 'B':
                        clinkBNum = 1
                        continue

                    elif list == 'C':
                        clinkCNum = 1
                        continue

                    elif list == 'D':
                        clinkDNum = 1
                        continue

            if isChoose == 3:
                if testAnswer[titleSe[page1 - 1].titleNo] == "True":
                    clinkTrue = 1
                else:
                    clinkTrue = 0
                if testAnswer[titleSe[page1 - 1].titleNo] == "False":
                    clinkFalse = 1
                else:
                    clinkFalse = 0
                if testAnswer[titleSe[page1 - 1].titleNo] == "":
                    clinkTrue = 0
                    clinkFalse = 0
            return redirect(url_for('web.beginSpecialTest', page=page1))

        if request.form["action"] == "下一题":
            page2 = page + 1
            if testAnswer[titleSe[page2 - 1].titleNo] == '' or testAnswer[titleSe[page2 - 1].titleNo] == []:
                clinkANum = 0
                clinkBNum = 0
                clinkCNum = 0
                clinkDNum = 0
                clinkTrue = 0
                clinkFalse = 0
            else:
                if isChoose == 1:
                    if testAnswer[titleSe[page2 - 1].titleNo] == "A":
                        clinkANum = 1
                    else:
                        clinkANum = 0
                    if testAnswer[titleSe[page2 - 1].titleNo] == "B":
                        clinkBNum = 1
                    else:
                        clinkBNum = 0
                    if testAnswer[titleSe[page2 - 1].titleNo] == "C":
                        clinkCNum = 1
                    else:
                        clinkCNum = 0
                    if testAnswer[titleSe[page2 - 1].titleNo] == "D":
                        clinkDNum = 1
                    else:
                        clinkDNum = 0
                    if testAnswer[titleSe[page2 - 1].titleNo] == ' ':
                        clinkANum = 0
                        clinkBNum = 0
                        clinkCNum = 0
                        clinkDNum = 0
                if isChoose == 2:
                    clinkANum = 0
                    clinkBNum = 0
                    clinkCNum = 0
                    clinkDNum = 0
                    for list in testAnswer[titleSe[page2 - 1].titleNo]:
                        if list == 'A':
                            clinkANum = 1
                            continue

                        elif list == 'B':
                            clinkBNum = 1
                            continue

                        elif list == 'C':
                            clinkCNum = 1
                            continue

                        elif list == 'D':
                            clinkDNum = 1
                            continue

                if isChoose == 3:
                    if testAnswer[titleSe[page2 - 1].titleNo] == "True":
                        clinkTrue = 1
                    else:
                        clinkTrue = 0
                    if testAnswer[titleSe[page2 - 1].titleNo] == "False":
                        clinkFalse = 1
                    else:
                        clinkFalse = 0
                    if testAnswer[titleSe[page2 - 1].titleNo] == "":
                        clinkTrue = 0
                        clinkFalse = 0
            return redirect(url_for('web.beginSpecialTest', page=page2))



        if request.form["action"] == "跳转":
            if form.gotoPage.data < 1:
                flash('没有零及负数页哦！')
                return redirect(url_for('web.beginSpecialTest', page=page))
            elif form.gotoPage.data > 20:
                flash('最多有20页哦！')
                return redirect(url_for('web.beginSpecialTest', page=page))
            else:
                if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == '' or testAnswer[
                    titleSe[form.gotoPage.data - 1].titleNo] == []:
                    clinkANum = 0
                    clinkBNum = 0
                    clinkCNum = 0
                    clinkDNum = 0
                    clinkTrue = 0
                    clinkFalse = 0
                else:
                    if isChoose == 1:
                        if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == "A":
                            clinkANum = 1
                        else:
                            clinkANum = 0
                        if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == "B":
                            clinkBNum = 1
                        else:
                            clinkBNum = 0
                        if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == "C":
                            clinkCNum = 1
                        else:
                            clinkCNum = 0
                        if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == "D":
                            clinkDNum = 1
                        else:
                            clinkDNum = 0
                        if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == ' ':
                            clinkANum = 0
                            clinkBNum = 0
                            clinkCNum = 0
                            clinkDNum = 0
                    if isChoose == 2:
                        clinkANum = 0
                        clinkBNum = 0
                        clinkCNum = 0
                        clinkDNum = 0
                        for list in testAnswer[titleSe[form.gotoPage.data - 1].titleNo]:
                            if list == 'A':
                                clinkANum = 1
                                continue

                            elif list == 'B':
                                clinkBNum = 1
                                continue

                            elif list == 'C':
                                clinkCNum = 1
                                continue

                            elif list == 'D':
                                clinkDNum = 1
                                continue

                    if isChoose == 3:
                        if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == "True":
                            clinkTrue = 1
                        else:
                            clinkTrue = 0
                        if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == "False":
                            clinkFalse = 1
                        else:
                            clinkFalse = 0
                        if testAnswer[titleSe[form.gotoPage.data - 1].titleNo] == "":
                            clinkTrue = 0
                            clinkFalse = 0

                return redirect(url_for('web.beginSpecialTest', page=form.gotoPage.data))


    return render_template('beginSpecialTest.html', title='专项测试', form = form, flag=classflag, isChoose=isChoose, page=page, titleSe=titleSe, clinkANum=clinkANum, clinkBNum=clinkBNum,
                           clinkCNum=clinkCNum, clinkDNum=clinkDNum, answer=answer, clinkTrue=clinkTrue,
                           clinkFalse=clinkFalse)




@webapp.route('/userInfo', methods=['GET','POST'])
def userInfo():
    uInfo = se.session.query(User).filter(User.id==g.user.id).first()
    form = UserInfo(request.form)
    if request.method == "POST":
        if request.form["action"] == "修改姓名":
            if form.updateName.data is None:
                flash("请填入要修改的姓名")
            else:
                se.session.query(User).filter(User.id==g.user.id).update({User.name: form.updateName.data}, synchronize_session=False)
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

        if request.form["action"] == "修改邮箱":
            if form.updateEmain.data is None:
                flash("请填入需要修改的邮箱")
            else:
                se.session.query(User).filter(User.id == g.user.id).update({User.Email: form.updateEmain.data},
                                                                           synchronize_session=False)
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

        if request.form["action"] == "修改电话":
            if form.updateTel.data is None:
                flash("请填入需要修改的电话")
            else:
                se.session.query(User).filter(User.id == g.user.id).update({User.tel: form.updateTel.data},
                                                                           synchronize_session=False)
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

        if request.form["action"]=="返回主界面":
            return redirect(url_for('web.main'))


    return render_template('userInfo.html', title='用户信息查询及修改', form=form, uInfo=uInfo)


@webapp.route('/adminMain', methods=['GET','POST'])
def adminMain():
    form = AdminMainForm(request.form)
    return render_template('adminMain.html', title='管理界面', form=form)


@webapp.route('/adminMain/userManager', methods=['GET','POST'])
def adminMainUserManager():
    # form = AdminUserManagerForm(request.form)
    return render_template('adminMainUserManager.html', title='用户管理')


@webapp.route('/adminMain/userManager/user/<int:page>', methods=['GET','POST'])
def managerUser(page):
    form = ManagerUser(request.form)

    i = 1
    # 用户数
    userNum = se.session.query(func.count(User.id)).scalar()
    # 单选页数
    pageNum = (int)(userNum / 10) + 1
    if page == None:
        page = 1
    if page < 1:
        page = 1
    if page > pageNum:
        page = pageNum
    pageSe = []
    while i <= pageNum:
        pageSe.append(i)
        i = i + 1
    showNum = se.session.query(User).slice((page-1)*10,10).all()
    if request.method == "POST":
        if request.form["action"] == "删除用户":
            if form.userAccount.data != "":
                x = se.session.query(User).filter(User.id == form.userAccount.data).first()

                if x is None:
                    flash("请输入正确的用户名")
                else:
                    se.session.delete(x)
                    try:
                        se.session.commit()
                    except:
                        se.session.rollback()
            else:
                flash('请输入用户账户')
        return redirect(url_for('web.managerUser', page=1))
    return render_template('ManagerUser.html', title='管理用户', page=page, form=form, pageNum=pageNum, showNum=showNum, pageSe=pageSe)


@webapp.route('/adminMain/adminManager/admin/<int:page>', methods=['GET','POST'])
def managerAdmin(page):
    form = ManagerAdmin(request.form)
    i = 1
    # 用户数
    adminNum = se.session.query(func.count(Admin.name)).scalar()
    # 单选页数
    pageNum = (int)(adminNum / 10) + 1
    if page == None:
        page = 1
    if page < 1:
        page = 1
    if page > pageNum:
        page = pageNum
    pageSe = []
    while i <= pageNum:
        pageSe.append(i)
        i = i + 1
    showNum = se.session.query(Admin).slice((page - 1) * 10 , 10).all()
    if request.method == "POST":
        if request.form["action"] == "添加管理员":
            if form.adminAccount.data != "" and form.adminPassword.data != "":
                insertAdmin = Admin(form.adminAccount.data, form.adminPassword.data)
                se.session.add(insertAdmin)
                try:
                    se.session.commit()
                except:
                    se.session.rollback()
                    flash("该数据以添加")
                return redirect(url_for('web.managerAdmin', page=1))
            else:
                flash("请输入所有数据")

            return redirect(url_for('web.managerAdmin', page=1))
        if request.form["action"] == "删除管理员":
            if form.adminAccount.data != "":
                x = se.session.query(Admin).filter(Admin.name == form.adminAccount.data).first()
                if x is None:
                    flash("请输入正确的管理员")
                else:
                    se.session.delete(x)
                    try:
                        se.session.commit()
                    except:
                        se.session.rollback()
                return redirect(url_for('web.managerAdmin', page=1))
            else:
                flash('请输入管理员账户')
    return render_template('ManagerAdmin.html', title='管理管理员', page=page, isChoose=isChoose, form=form, pageNum=pageNum, showNum=showNum,
                           pageSe=pageSe)


@webapp.route('/adminMain/titleManager', methods=['GET','POST'])
def adminMainTitleManager():
    return render_template('adminMainTitleManager.html', title='题库管理')
#同上
@webapp.route('/adminMain/titleManager', methods=['GET','POST'])
def titleManager():
    render_template('adminMainTitleManager.html', title="题库管理")



@webapp.route('/adminMain/titleManager/oneChoose/<int:page>', methods=['GET','POST'])
def titleOneChoose(page):
    i = 1
    form = OneChooseTitle(request.form)
    # 单选题目数
    oneChooseNum = se.session.query(func.count(OneChooseItem.titleNo)).scalar()
    # 单选页数
    pageNum = (int)(oneChooseNum/10) + 1
    if page == None:
        page=1
    if page < 1:
        page = 1
    if page > pageNum:
        page=pageNum
    pageSe = []
    while i<=pageNum:
        pageSe.append(i)
        i = i + 1
    showNum = se.session.query(OneChooseItem).filter((OneChooseItem.titleNo-100000+1) >= (page-1)*10 + 1).filter((OneChooseItem.titleNo-100000+1) <= (page*10)).all()




    if request.method == "POST":
        if request.form["action"] == "增加单选题":
            if form.oneChooseTitleNo.data is not None and form.oneChooseAnswer.data is not None and form.oneChooseChooseA.data is not None and form.oneChooseChooseB.data is not None and form.oneChooseChooseC.data is not None and form.oneChooseChooseD.data is not None and form.oneChooseContent.data:

                insOneChoose = OneChooseItem(titleNo=form.oneChooseTitleNo.data, content=form.oneChooseContent.data,
                                            chooseA=form.oneChooseChooseA.data,chooseB=form.oneChooseChooseB.data,chooseC=form.oneChooseChooseC.data,
                                             chooseD=form.oneChooseChooseD.data,
                                              answer=form.oneChooseAnswer.data, category=form.oneChooseCategory.data)
                se.session.add(insOneChoose)
                try:
                    se.session.commit()
                except:
                    se.session.rollback()
                return redirect(url_for('web.titleOneChoose', page=1))
            else:
                flash('请填入所有信息')

        if request.form["action"] == "删除单选题":
            if form.oneChooseTitleNo.data is not None:
                x = se.session.query(OneChooseItem).filter(OneChooseItem.titleNo == form.oneChooseTitleNo.data).one()
                se.session.delete(x)
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

                return redirect(url_for('web.titleOneChoose', page=1))
            else:
                flash('请输入所要删除的题号')

        if request.form["action"] == "修改单选题答案":
            if form.oneChooseTitleNo.data is not None and form.oneChooseAnswer.data is not None:
                upOneChoose = se.session.query(OneChooseItem).filter(OneChooseItem.titleNo == form.oneChooseTitleNo.data).first()
                upOneChoose.answer = form.oneChooseAnswer.data
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

            else:
                flash('请输入所要修改的题号和答案')

        if request.form["action"] == "修改单选题选项A":
            if form.oneChooseChooseA.data is not None and form.oneChooseTitleNo.data is not None:
                upOneChoose = se.session.query(OneChooseItem).filter(OneChooseItem.titleNo == form.oneChooseTitleNo.data).first()
                upOneChoose.chooseA = form.oneChooseChooseA.data
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

            else:
                flash('请输入所要修改的题号和选项A')

        if request.form["action"] == "修改单选题选项B":
            if form.oneChooseChooseB.data is not None and form.oneChooseTitleNo.data is not None:
                upOneChoose = se.session.query(OneChooseItem).filter(OneChooseItem.titleNo == form.oneChooseTitleNo.data).first()
                upOneChoose.chooseB = form.oneChooseChooseB.data
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

            else:
                flash('请输入所要修改的题号和选项B')

        if request.form["action"] == "修改单选题选项C":
            if form.oneChooseChooseC.data is not None and form.oneChooseTitleNo.data is not None:
                upOneChoose = se.session.query(OneChooseItem).filter(OneChooseItem.titleNo == form.oneChooseTitleNo.data).first()
                upOneChoose.chooseC = form.oneChooseChooseC.data
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

            else:
                flash('请输入所要修改的题号和选项C')

        if request.form["action"] == "修改单选题选项D":
            if form.oneChooseChooseD.data is not None and form.oneChooseTitleNo.data is not None:
                upOneChoose = se.session.query(OneChooseItem).filter(OneChooseItem.titleNo == form.oneChooseTitleNo.data).first()
                upOneChoose.chooseD = form.oneChooseChooseD.data
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

                return redirect(url_for('web.titleOneChoose', page=1))
            else:
                flash('请输入所要修改的题号和选项D')

        if request.form["action"] == "修改单选题内容":
            if form.oneChooseContent.data is not None and form.oneChooseTitleNo.data is not None:
                upOneChoose = se.session.query(OneChooseItem).filter(OneChooseItem.titleNo == form.oneChooseTitleNo.data).first()
                upOneChoose.content = form.oneChooseContent.data
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

            else:
                flash('请输入所要修改的题号和内容')


        if request.form["action"] == "修改单选题类别":
            if form.oneChooseCategory.data is not None and form.oneChooseTitleNo.data is not None:
                upOneChoose = se.session.query(OneChooseItem).filter(OneChooseItem.titleNo == form.oneChooseTitleNo.data).first()
                upOneChoose.category = form.oneChooseCategory.data
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

            else:
                flash('请输入所要修改的题号和类别')


    return render_template('titleManagerOneChoose.html', title='单选题库', form = form, page=page, pageNum=pageNum, showNum=showNum, pageSe=pageSe)


@webapp.route('/adminMain/titleManager/manyChoose/<int:page>', methods=['GET','POST'])
def titleManyChoose(page):
    i = 1
    form = ManyChooseTitle(request.form)
    # 单选题目数
    manyChooseNum = se.session.query(func.count(ManyChooseItem.titleNo)).scalar()
    # 单选页数
    pageNum = (int)(manyChooseNum/10) + 1
    if page == None:
        page=1
    if page < 1:
        page = 1
    if page > pageNum:
        page=pageNum
    pageSe = []
    while i<=pageNum:
        pageSe.append(i)
        i = i + 1
    showNum = se.session.query(ManyChooseItem).filter((ManyChooseItem.titleNo-200000 +1) >= (page-1)*10 + 1).filter((ManyChooseItem.titleNo-200000+1) <= (page*10)).all()
    print(showNum)

    if request.method == "POST":
        if request.form["action"] == "增加多选题":
            if form.manyChooseTitleNo.data is not None and form.manyChooseAnswer.data is not None and form.manyChooseChooseA.data is not None and form.manyChooseChooseB.data is not None and form.manyChooseChooseC.data is not None and form.manyChooseChooseD.data is not None and form.manyChooseContent.data:

                insManyChoose = ManyChooseItem(titleNo=form.manyChooseTitleNo.data, content=form.manyChooseContent.data,
                                            chooseA=form.manyChooseChooseA.data,chooseB=form.manyChooseChooseB.data,chooseC=form.manyChooseChooseC.data,
                                             chooseD=form.manyChooseChooseD.data,
                                              answer=form.manyChooseAnswer.data, category=form.manyChooseCategory.data)

                se.session.add(insManyChoose)
                try:
                    se.session.commit()
                except:
                    se.session.rollback()
                return redirect(url_for('web.titleManyChoose', page=1))
            else:
                flash('请填入所有信息')

        if request.form["action"] == "删除多选题":
            if form.manyChooseTitleNo.data is not None:
                x = se.session.query(ManyChooseItem).filter(ManyChooseItem.titleNo == form.manyChooseTitleNo.data).first()
                se.session.delete(x)
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

                return redirect(url_for('web.titleManyChoose', page=1))
            else:
                flash('请输入所要删除的题号')

        if request.form["action"] == "修改多选题答案":
            if form.manyChooseTitleNo.data is not None and form.manyChooseAnswer.data is not None:
                upManyChoose = se.session.query(ManyChooseItem).filter(ManyChooseItem.titleNo == form.manyChooseTitleNo.data).first()
                upManyChoose.answer = form.manyChooseAnswer.data
                se.session.commit()


            else:
                flash('请填入题号和多选题答案')

        if request.form["action"] == "修改多选题选项A":
            if form.manyChooseChooseA.data is not None and form.manyChooseTitleNo.data is not None :
                upManyChoose = se.session.query(ManyChooseItem).filter(ManyChooseItem.titleNo == form.manyChooseTitleNo.data).first()
                upManyChoose.chooseA = form.manyChooseChooseA.data
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

            else:
                flash('请填入题号和多选题选项A')


        if request.form["action"] == "修改多选题选项B":
            if form.manyChooseChooseB.data is not None and form.manyChooseTitleNo.data is not None :
                upManyChoose = se.session.query(ManyChooseItem).filter(ManyChooseItem.titleNo == form.manyChooseTitleNo.data).first()
                upManyChoose.chooseB = form.manyChooseChooseB.data
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

            else:
                flash('请填入题号和多选题选项B')


        if request.form["action"] == "修改多选题选项C":
            if form.manyChooseChooseC.data is not None and form.manyChooseTitleNo.data is not None :
                upManyChoose = se.session.query(ManyChooseItem).filter(ManyChooseItem.titleNo == form.manyChooseTitleNo.data).first()
                upManyChoose.chooseC = form.manyChooseChooseC.data
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

            else:
                flash('请填入题号和多选题选项C')

        if request.form["action"] == "修改多选题选项D":
            if form.manyChooseChooseD.data is not None and form.manyChooseTitleNo.data is not None:
                upManyChoose = se.session.query(ManyChooseItem).filter(ManyChooseItem.titleNo == form.manyChooseTitleNo.data).first()
                upManyChoose.chooseD = form.manyChooseChooseD.data
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

                return redirect(url_for('web.titleManyChoose', page=1))

            else:
                flash('请填入题号和多选题选项D')

        if request.form["action"] == "修改多选题内容":
            if form.manyChooseContent.data is not None and form.manyChooseTitleNo.data is not None:
                upManyChoose = se.session.query(ManyChooseItem).filter(ManyChooseItem.titleNo == form.manyChooseTitleNo.data).first()
                upManyChoose.content = form.manyChooseContent.data
                try:
                    se.session.commit()
                except:
                    se.session.rollback()


            else:
                flash('请填入题号和多选题内容')

        if request.form["action"] == "修改多选题类别":
            if form.manyChooseCategory.data is not None and form.manyChooseTitleNo.data is not None:
                upManyChoose = se.session.query(ManyChooseItem).filter(ManyChooseItem.titleNo == form.manyChooseTitleNo.data).first()
                upManyChoose.category = form.manyChooseCategory.data
                try:
                    se.session.commit()
                except:
                    se.session.rollback()


            else:
                flash('请填入题号和多选题内容')

    return render_template('titleManagerManyChoose.html', title='多选题库', form = form, page=page, pageNum=pageNum, showNum=showNum, pageSe=pageSe)


@webapp.route('/adminMain/titleManager/judge/<int:page>', methods=['GET','POST'])
def titleJudge(page):
    i = 1
    form = JudgeTitle(request.form)
    # 单选题目数
    judgeNum = se.session.query(func.count(turefalseItem.titleNo)).scalar()
    # 单选页数
    pageNum = (int)(judgeNum/10) + 1
    if page == None:
        page=1
    if page < 1:
        page = 1
    if page > pageNum:
        page=pageNum
    pageSe = []
    while i<=pageNum:
        pageSe.append(i)
        i = i + 1
    showNum = se.session.query(turefalseItem).filter((turefalseItem.titleNo-300000+1) >= (page-1)*10 + 1).filter((turefalseItem.titleNo-300000+1) <= (page*10)).all()


    if request.method == "POST":
        if request.form["action"] == "增加判断题":
            if form.judgeTitleNo.data is not None and form.judgeAnswer.data is not None and form.judgeContent.data:

                insManyChoose = turefalseItem(titleNo=form.judgeTitleNo.data, content=form.judgeContent.data,
                                              answer=form.judgeAnswer.data, category=form.judgeCategory.data)
                se.session.add(insManyChoose)
                try:
                    se.session.commit()
                except:
                    se.session.rollback()
                return redirect(url_for('web.titleJudge', page=1))
            else:
                flash('请填入所有信息')

        if request.form["action"] == "删除判断题":
            if form.judgeTitleNo.data is not None:
                x2=se.session.query(turefalseItem).filter(turefalseItem.titleNo == form.judgeTitleNo.data).one()
                se.session.delete(x2)
                try:
                    se.session.commit()
                except:
                    se.session.rollback()

                return redirect(url_for('web.titleJudge', page=1))
            else:
                flash('请输入所要删除的题号')

        if request.form["action"] == "修改判断题答案":
            if form.judgeAnswer.data is not None and form.judgeTitleNo.data is not None:
                upJudge = se.session.query(turefalseItem).filter(
                    turefalseItem.titleNo == form.judgeTitleNo.data).first()
                upJudge.answer = form.judgeAnswer.data
                try:
                    se.session.commit()
                except:
                    se.session.rollback()
            else:
                flash('请填入修改的判断题答案和题号')

        if request.form["action"] == "修改判断题题目":
            if form.judgeTitleNo.data is not None and form.judgeContent.data is not None:
                upJudge = se.session.query(turefalseItem).filter(turefalseItem.titleNo == form.judgeTitleNo.data).first()
                upJudge.content = form.judgeContent.data
                try:
                    se.session.commit()
                except:
                    se.session.rollback()
            else:
                flash('请填入修改的判断题题目和题号')


        if request.form["action"] == "修改判断题类别":
            if form.judgeCategory.data is not None and form.judgeTitleNo.data is not None:
                upJudge = se.session.query(turefalseItem).filter(turefalseItem.titleNo == form.judgeTitleNo.data).first()
                upJudge.category = form.judgeCategory.data
                try:
                    se.session.commit()
                except:
                    se.session.rollback()


            else:
                flash('请填入题号和判断题内容')

        return redirect(url_for('web.titleJudge', page=1))
    return render_template('titleManagerJudge.html', title='判断题库', form = form, page=page, pageNum=pageNum, showNum=showNum, pageSe=pageSe)




@webapp.route('/adminMain/searchResult/', methods=['GET','POST'])
def adminMainSearchResult():
    return render_template('adminMainSearchResult.html', title='成绩查询')


# 查询类别
searchOne = 0
@webapp.route('/adminMain/searchResult/searchOneChooseResult/<int:page>', methods=['GET','POST'])
def searchOneChooseResult(page):
    global searchOne
    form = OneChooseResult(request.form)
    oneInfo = ""
    totalNum1 = 0
    if request.method == "POST":
        if request.form["action"] == "查询":

            if form.searchClass.data == '1' or searchOne == 1:
                searchOne = 1
                oneInfo = se.session.query(TestRecord.TestNum, User.id, TestRecord.startTime, OneChooseItem.titleNo,
                                           oneChooseOperate.isCorrect).filter(
                    TestRecord.TestNum == Search.TestNum).filter(User.id == Search.id).filter(
                    TestRecord.TestNum == oneChooseOperate.TestNum_1).filter(
                    oneChooseOperate.titleNo_1 == OneChooseItem.titleNo).filter(OneChooseItem.titleNo == form.searchContent.data).slice(
                    (page - 1) * 60, page * 60)
                totalNum1 = se.session.query(func.count('*').label('count')).filter(
                    Search.TestNum == TestRecord.TestNum).filter(Search.id == User.id).filter(
                    TestRecord.TestNum == oneChooseOperate.TestNum_1).filter(
                    oneChooseOperate.titleNo_1 == OneChooseItem.titleNo).filter(OneChooseItem.titleNo == int(form.searchContent.data)).scalar()

            if form.searchClass.data == '2' or searchOne == 2:
                searchOne = 2
                oneInfo = se.session.query(TestRecord.TestNum, User.id, TestRecord.startTime, OneChooseItem.titleNo,
                                           oneChooseOperate.isCorrect).filter(
                    TestRecord.TestNum == Search.TestNum).filter(User.id == Search.id).filter(
                    TestRecord.TestNum == oneChooseOperate.TestNum_1).filter(
                    oneChooseOperate.titleNo_1 == OneChooseItem.titleNo).filter(
                    User.id == form.searchContent.data).slice(
                    (page - 1) * 60, page * 60)
                totalNum1 = se.session.query(func.count('*').label('count')).filter(
                    Search.TestNum == TestRecord.TestNum).filter(Search.id == User.id).filter(
                    TestRecord.TestNum == oneChooseOperate.TestNum_1).filter(
                    oneChooseOperate.titleNo_1 == OneChooseItem.titleNo).filter(
                    User.id == form.searchContent.data).scalar()

            if form.searchClass.data == '3' or searchOne == 3:
                searchOne = 3
                oneInfo = se.session.query(TestRecord.TestNum, User.id, TestRecord.startTime, OneChooseItem.titleNo,
                                           oneChooseOperate.isCorrect).filter(
                    TestRecord.TestNum == Search.TestNum).filter(User.id == Search.id).filter(
                    TestRecord.TestNum == oneChooseOperate.TestNum_1).filter(
                    oneChooseOperate.titleNo_1 == OneChooseItem.titleNo).filter(TestRecord.TestNum == int(form.searchContent.data)
                    ).slice(
                    (page - 1) * 60, page * 60)
                totalNum1 = se.session.query(func.count('*').label('count')).filter(
                    Search.TestNum == TestRecord.TestNum).filter(Search.id == User.id).filter(
                    TestRecord.TestNum == oneChooseOperate.TestNum_1).filter(
                    oneChooseOperate.titleNo_1 == OneChooseItem.titleNo).filter(
                    TestRecord.TestNum == int(form.searchContent.data)).scalar()
    else:
        searchOne = 0
        oneInfo = se.session.query(TestRecord.TestNum, User.id, TestRecord.startTime, OneChooseItem.titleNo, oneChooseOperate.isCorrect).filter(TestRecord.TestNum == Search.TestNum).filter(User.id == Search.id).filter(TestRecord.TestNum == oneChooseOperate.TestNum_1).filter(oneChooseOperate.titleNo_1 == OneChooseItem.titleNo).order_by(TestRecord.TestNum).slice((page-1)*60, page*60)
        totalNum1 = se.session.query(func.count('*').label('count')).filter(Search.TestNum == TestRecord.TestNum).filter(Search.id == User.id).filter(TestRecord.TestNum == oneChooseOperate.TestNum_1).filter(oneChooseOperate.titleNo_1 == OneChooseItem.titleNo).scalar()

    pageNum = totalNum1 / 60
    if page == 0:
        page = 1
    if page == None:
        page = 1
    if page < 1:
        page = 1
    if page > pageNum:
        page = pageNum
    pageSe = []
    i = 1
    while i <= pageNum:
        pageSe.append(i)
        i = i + 1

    return render_template('searchOneChooseResult.html', title='单选成绩查询', page=page, pageSe=pageSe, oneInfo=oneInfo, form = form)


@webapp.route('/adminMain/searchResult/searchManyChooseResult/<int:page>', methods=['GET','POST'])
def searchManyChooseResult(page):
    form = ManyChooseResult(request.form)
    manyInfo = ""
    totalNum2 = 0
    if request.method == "POST":
        if request.form["action"] == "查询":
            if form.searchClass.data == '1':
                manyInfo = se.session.query(TestRecord.TestNum, User.id, TestRecord.startTime, ManyChooseItem.titleNo,
                                            manyChooseOperate.isCorrect).filter(
                    TestRecord.TestNum == Search.TestNum).filter(
                    User.id == Search.id).filter(TestRecord.TestNum == manyChooseOperate.TestNum_2).filter(
                    manyChooseOperate.titleNo_2 == ManyChooseItem.titleNo).filter(ManyChooseItem.titleNo == form.searchContent.data).slice(
                    (page - 1) * 60, page * 60)
                totalNum2 = se.session.query(func.count('*').label('count')).filter(
                    Search.TestNum == TestRecord.TestNum).filter(
                    Search.id == User.id).filter(TestRecord.TestNum == manyChooseOperate.TestNum_2).filter(
                    manyChooseOperate.titleNo_2 == ManyChooseItem.titleNo).filter(ManyChooseItem.titleNo == form.searchContent.data).scalar()

            if form.searchClass.data == '2':
                manyInfo = se.session.query(TestRecord.TestNum, User.id, TestRecord.startTime, ManyChooseItem.titleNo,
                                            manyChooseOperate.isCorrect).filter(
                    TestRecord.TestNum == Search.TestNum).filter(
                    User.id == Search.id).filter(TestRecord.TestNum == manyChooseOperate.TestNum_2).filter(
                    manyChooseOperate.titleNo_2 == ManyChooseItem.titleNo).filter(
                    User.id == form.searchContent.data).slice(
                    (page - 1) * 60, page * 60)
                totalNum2 = se.session.query(func.count('*').label('count')).filter(
                    Search.TestNum == TestRecord.TestNum).filter(
                    Search.id == User.id).filter(TestRecord.TestNum == manyChooseOperate.TestNum_2).filter(
                    manyChooseOperate.titleNo_2 == ManyChooseItem.titleNo).filter(
                    User.id == form.searchContent.data).scalar()

            if form.searchClass.data == '3':
                manyInfo = se.session.query(TestRecord.TestNum, User.id, TestRecord.startTime, ManyChooseItem.titleNo,
                                            manyChooseOperate.isCorrect).filter(
                    TestRecord.TestNum == Search.TestNum).filter(
                    User.id == Search.id).filter(TestRecord.TestNum == manyChooseOperate.TestNum_2).filter(
                    manyChooseOperate.titleNo_2 == ManyChooseItem.titleNo).filter(
                    TestRecord.TestNum == int(form.searchContent.data)).slice(
                    (page - 1) * 60, page * 60)
                totalNum2 = se.session.query(func.count('*').label('count')).filter(
                    Search.TestNum == TestRecord.TestNum).filter(
                    Search.id == User.id).filter(TestRecord.TestNum == manyChooseOperate.TestNum_2).filter(
                    manyChooseOperate.titleNo_2 == ManyChooseItem.titleNo).filter(
                    TestRecord.TestNum == int(form.searchContent.data)).scalar()

    else:
        manyInfo = se.session.query(TestRecord.TestNum, User.id, TestRecord.startTime, ManyChooseItem.titleNo,
                                manyChooseOperate.isCorrect).filter(TestRecord.TestNum == Search.TestNum).filter(
                                User.id == Search.id).filter(TestRecord.TestNum == manyChooseOperate.TestNum_2).filter(
                                manyChooseOperate.titleNo_2 == ManyChooseItem.titleNo).order_by(TestRecord.TestNum).slice((page-1)*60, page*60)
        totalNum2 = se.session.query(func.count('*').label('count')).filter(Search.TestNum == TestRecord.TestNum).filter(
                                Search.id == User.id).filter(TestRecord.TestNum == manyChooseOperate.TestNum_2).filter(
                                manyChooseOperate.titleNo_2 == ManyChooseItem.titleNo).scalar()
    pageNum = totalNum2 / 60
    if page == 0:
        page = 1
    if page == None:
        page = 1
    if page < 1:
        page = 1
    if page > pageNum:
        page = pageNum
    pageSe = []
    i = 1
    while i <= pageNum:
        pageSe.append(i)
        i = i + 1
    return render_template('searchManyChooseResult.html', title='多选成绩查询', page=page, pageSe=pageSe, manyInfo=manyInfo, form=form)

@webapp.route('/adminMain/searchResult/searchJudgeResult/<int:page>', methods=['GET','POST'])
def searchJudgeResult(page):
    form = JudgeResult(request.form)
    judgeInfo = ""
    totalNum3 = 0

    if request.method == "POST":
        if request.form["action"] == "查询":
            if form.searchClass.data == '1':
                judgeInfo = se.session.query(TestRecord.TestNum, User.id, TestRecord.startTime, turefalseItem.titleNo,
                                             judgeOperate.isCorrect).filter(
                    TestRecord.TestNum == Search.TestNum).filter(User.id == Search.id).filter(
                    TestRecord.TestNum == judgeOperate.TestNum_3).filter(
                    judgeOperate.titleNo_3 == turefalseItem.titleNo).filter(turefalseItem.titleNo == int(form.searchContent.data)).slice((page - 1) * 60,
                                                                                                        page * 60)
                totalNum3 = se.session.query(func.count('*').label('count')).filter(
                    Search.TestNum == TestRecord.TestNum).filter(
                    Search.id == User.id).filter(TestRecord.TestNum == judgeOperate.TestNum_3).filter(
                    judgeOperate.titleNo_3 == turefalseItem.titleNo).filter(turefalseItem.titleNo == int(form.searchContent.data)).scalar()
            if form.searchClass.data == '2':
                judgeInfo = se.session.query(TestRecord.TestNum, User.id, TestRecord.startTime, turefalseItem.titleNo,
                                             judgeOperate.isCorrect).filter(
                    TestRecord.TestNum == Search.TestNum).filter(User.id == Search.id).filter(
                    TestRecord.TestNum == judgeOperate.TestNum_3).filter(
                    judgeOperate.titleNo_3 == turefalseItem.titleNo).filter(
                    User.id == form.searchContent.data).slice((page - 1) * 60,
                                                                            page * 60)
                totalNum3 = se.session.query(func.count('*').label('count')).filter(
                    Search.TestNum == TestRecord.TestNum).filter(
                    Search.id == User.id).filter(TestRecord.TestNum == judgeOperate.TestNum_3).filter(
                    judgeOperate.titleNo_3 == turefalseItem.titleNo).filter(
                    User.id == form.searchContent.data).scalar()
            if form.searchClass.data == '3':
                judgeInfo = se.session.query(TestRecord.TestNum, User.id, TestRecord.startTime, turefalseItem.titleNo,
                                             judgeOperate.isCorrect).filter(
                    TestRecord.TestNum == Search.TestNum).filter(User.id == Search.id).filter(
                    TestRecord.TestNum == judgeOperate.TestNum_3).filter(
                    judgeOperate.titleNo_3 == turefalseItem.titleNo).filter(
                    TestRecord.TestNum == int(form.searchContent.data)).slice((page - 1) * 60,
                                                                            page * 60)
                totalNum3 = se.session.query(func.count('*').label('count')).filter(
                    Search.TestNum == TestRecord.TestNum).filter(
                    Search.id == User.id).filter(TestRecord.TestNum == judgeOperate.TestNum_3).filter(
                    judgeOperate.titleNo_3 == turefalseItem.titleNo).filter(
                    TestRecord.TestNum == int(form.searchContent.data)).scalar()

    else:
        judgeInfo = se.session.query(TestRecord.TestNum, User.id, TestRecord.startTime,turefalseItem.titleNo, judgeOperate.isCorrect).filter(
                   TestRecord.TestNum == Search.TestNum).filter(User.id == Search.id).filter(
                   TestRecord.TestNum == judgeOperate.TestNum_3).filter(judgeOperate.titleNo_3 == turefalseItem.titleNo).order_by(TestRecord.TestNum).slice((page-1)*60, page*60)
        totalNum3 = se.session.query(func.count('*').label('count')).filter(Search.TestNum == TestRecord.TestNum).filter(
                   Search.id == User.id).filter(TestRecord.TestNum == judgeOperate.TestNum_3).filter(
                judgeOperate.titleNo_3 == turefalseItem.titleNo).scalar()
    pageNum = totalNum3 / 60
    if page == 0:
        page = 1
    if page == None:
        page = 1
    if page < 1:
        page = 1
    if page > pageNum:
        page = pageNum
    pageSe = []
    i = 1
    while i <= pageNum:
        pageSe.append(i)
        i = i + 1
    return render_template('searchJudgeResult.html', title='判断成绩查询', page=page, pageSe=pageSe, judgeInfo=judgeInfo, form=form)


# @webapp.route('/adminMain/managerTest', methods=['GET','POST'])
# def adminMainManagerTest():
#     form = AdminManagerTestForm(request.form)
#     if request.method == "POST":
#         print(1)
#     return render_template('adminMainManagerTest.html', title='考试管理', form=form)