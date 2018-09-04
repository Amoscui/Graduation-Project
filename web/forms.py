from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField,IntegerField,RadioField, SelectField
from wtforms.validators import DataRequired, Email, length, Regexp, EqualTo



class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()])
    submit = SubmitField(label='登录')

class RegistrationForm(FlaskForm):
    account = StringField('账号', validators=[DataRequired(message='用户名必须由字母、数字、下划线或.组成'), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'用户名必须由字母、数字、下划线或.组成')])
    uname = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', '密码必须相同')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(message='邮箱不能为空'),length(1, 64), Email(message='请输入有效的邮箱地址')])
    sex = RadioField('性别', choices=[('0', '男'), ('1', '女')], validators=[DataRequired()], default='0')
    tel = StringField('电话', validators=[DataRequired(message='电话为11位号码'), length(11,11)])
    submit = SubmitField('提交')

class ForgetPasswordForm(FlaskForm):
    account = StringField('账号', validators=[DataRequired()])
    newPassword = PasswordField('新密码', validators=[DataRequired()])
    okPassword = PasswordField('确认密码', validators=[DataRequired(), EqualTo('newPassword', message='密码必须相同')])
    submit = SubmitField('确认')
    submit1 = SubmitField('确定')

class AdminLoginForm(FlaskForm):
    adminname = StringField('用户名', validators=[DataRequired()])
    password = PasswordField("密码", validators=[DataRequired()])
    submit = SubmitField(label='登录')


class MainForm(FlaskForm):
    a = StringField('a', validators=[DataRequired()])
    computer = SubmitField('计算机')


class BeginTestForm(FlaskForm):
    gotoPage = IntegerField('跳转', validators=[DataRequired()])


class BeginSpecialTestForm(FlaskForm):
    gotoPage = IntegerField('跳转', validators=[DataRequired()])



class UserInfo(FlaskForm):
    updateName = StringField('修改用户名', validators=[DataRequired()])
    updateEmain = StringField('修改邮箱', validators=[DataRequired(), Email()])
    updateTel = IntegerField('修改电话', validators=[DataRequired(), length(1,11)])



class AdminMainForm(FlaskForm):
    submit = SubmitField(label='登录')


class AdminManagerTestForm(FlaskForm):
    submit = SubmitField(label='登录')


class OneChooseTitle(FlaskForm):
    oneChooseTitleNo = IntegerField('单选题目编号', validators=[DataRequired()])
    oneChooseContent = StringField('单选题目', validators=[DataRequired()])
    oneChooseChooseA = StringField('单选选项A', validators=[DataRequired()])
    oneChooseChooseB = StringField('单选选项B', validators=[DataRequired()])
    oneChooseChooseC = StringField('单选选项C', validators=[DataRequired()])
    oneChooseChooseD = StringField('单选选项D', validators=[DataRequired()])
    oneChooseAnswer = StringField('单选答案', validators=[DataRequired()])
    oneChooseCategory = StringField('单选类别', validators=[DataRequired()])

class ManyChooseTitle(FlaskForm):
    manyChooseTitleNo = IntegerField('多选题目编号', validators=[DataRequired()])
    manyChooseContent = StringField('多选题目', validators=[DataRequired()])
    manyChooseChooseA = StringField('多选选项A', validators=[DataRequired()])
    manyChooseChooseB = StringField('多选选项B', validators=[DataRequired()])
    manyChooseChooseC = StringField('多选选项C', validators=[DataRequired()])
    manyChooseChooseD = StringField('多选选项D', validators=[DataRequired()])
    manyChooseAnswer = StringField('多选答案', validators=[DataRequired()])
    manyChooseCategory = StringField('多选类别', validators=[DataRequired()])


class ManagerUser(FlaskForm):
    userAccount = StringField('用户账号', validators=[DataRequired()])


class ManagerAdmin(FlaskForm):
    adminAccount = StringField('管理员账号', validators=[DataRequired()])
    adminPassword = StringField('密码', validators=[DataRequired()])


class JudgeTitle(FlaskForm):
    judgeTitleNo = IntegerField('判断题目编号', validators=[DataRequired()])
    judgeContent = StringField('判断题目', validators=[DataRequired()])
    judgeAnswer = StringField('判断答案', validators=[DataRequired()])
    judgeCategory = StringField('判断类别', validators=[DataRequired()])

# class AdminSearchResultForm(FlaskForm):
#     submit = SubmitField(label='登录')
#
# class AdminTitleManagerForm(FlaskForm):
#     submit = SubmitField(label='登录')
#
# class AdminUserManagerForm(FlaskForm):
#     submit = SubmitField(label='登录')
#
class OneChooseResult(FlaskForm):
    searchClass = SelectField('查询类别', choices=[
        ('1', '题号'),
        ('2', '用户'),
        ('3', '测试编号')
    ])
    searchContent = StringField('查询内容', validators=[DataRequired()])

class ManyChooseResult(FlaskForm):
    searchClass = SelectField('查询类别', choices=[
        ('1', '题号'),
        ('2', '用户'),
        ('3', '测试编号')
    ])
    searchContent = StringField('查询内容', validators=[DataRequired()])

class JudgeResult(FlaskForm):
    searchClass = SelectField('查询类别', choices=[
        ('1', '题号'),
        ('2', '用户'),
        ('3', '测试编号')
    ])
    searchContent = StringField('查询内容', validators=[DataRequired()])