from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import SelectMultipleField, SelectField, TextAreaField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from jobplus.customfield import TagListField, CityListField
from jobplus.models import db, User, Job,  get_salary_range
from jobplus.models import Jtag, Jcity, Salary_Range

import re

class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(1,24)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(),Length(6,24)])
    repeat_password = PasswordField('重复密码', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('提交')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')

    def create_user(self,register_role):
        user = User(
            username=self.username.data,
            email=self.email.data,
            password=self.password.data,
            role=register_role
        )
        db.session.add(user)
        db.session.commit()
        return user


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交') 

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱未注册')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码错误')



class TagForm(FlaskForm):
    
    name = StringField('名称', validators=[DataRequired(), Length(1,20)])




class AddTagForm(TagForm):
    tag_submit = SubmitField('提交')

    def validate_name(self, field):
        if Jtag.query.filter_by(name=field.data).first():
            raise ValidationError('标签已经存在.')

    def addtag(self):
        tag = Jtag(name=self.name.data)
        db.session.add(tag)
        db.session.commit()



class AddCityForm(TagForm):
    city_submit = SubmitField('提交')

    def validate_name(self, field):
        if Jcity.query.filter_by(name=field.data).first():
            raise ValidationError('城市已经存在.')


    def addtag(self):
        tag = Jcity(name=self.name.data)
        db.session.add(tag)
        db.session.commit()



class AddSalaryForm(TagForm):
    salary_submit  = SubmitField('提交')

    def validate_name(self, field):
        reg = re.compile(r'\d+--\d+')
        if not reg.fullmatch(field.data):
            raise ValidationError('请输入<数值>--<数值>')

        if Salary_Range.query.filter_by(name=field.data).first():
            raise ValidationError('薪资范围已经存在.')


    def addtag(self):
        tag = Salary_Range(name=self.name.data)
        db.session.add(tag)
        db.session.commit()


class JobForm(FlaskForm):
    name = StringField('岗位名称', validators=[DataRequired(), Length(1, 32)])
    requirements = TextAreaField('工作要求', validators=[DataRequired(), Length(1, 1024)])
    salary_range = QuerySelectField('薪资范围', query_factory=get_salary_range, get_label='srrange')
    tags = TagListField('关键字')
    cities = CityListField('工作地点')
    submit = SubmitField('提交')










    
