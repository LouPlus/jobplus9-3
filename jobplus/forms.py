from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import SelectMultipleField, SelectField, TextAreaField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError, URL

from jobplus.models import db, User, Job , Company
from jobplus.models import Jtag, Jcity, Salary_Range

from wtforms.ext.sqlalchemy.orm import model_form
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

class CompanyProfileForm(FlaskForm):
    name = StringField("Company name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone_number = StringField("Phone number", validators=[DataRequired(), Length(11)])
    address = StringField("Address", validators=[DataRequired()])
    website = StringField("Website address", validators=[DataRequired()])
    logo = StringField("Image url", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    info = StringField("Company info", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def update_company(self):
        company = Company(name = self.name.data,
        address = self.address.data,
        website = self.website.data,
        url = self.logo.data,
        description = self.description.data,
        user_id = current_user.id
        )
        db.session.add(company)
        db.session.commit()
        return company

class TagForm(FlaskForm):

    name = StringField('名称', validators=[DataRequired(), Length(1,20)])


    def updatetag(self, tag):
        self.populate_obj(tag)
        db.session.add(tag)
        db.session.commit()




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
    salary_submit = SubmitField('提交')

    def validate_name(self, field):
        reg = re.compile(r'(\d+)--(\d+)')
        if not reg.match(field.data):
            raise ValidationError('请输入<数值>--<数值>')

        if Salary_Range.query.filter_by(name=field.data).first():
            raise ValidationError('薪资范围已经存在.')


    def addtag(self):
        tag = Salary_Range(name=self.name.data)
        db.session.add(tag)
        db.session.commit()




JobForm = model_form(Job,
                     db_session=db.session, base_class=FlaskForm,
                     only=['name','requirements', 'tags', 'cities', 'salary_range', 'company'],
                     field_args =
                     {
                        'name': { 'label':'岗位名称', 'validators':[DataRequired(), Length(1, 32)]},
                        'requirements': {'label':'职位要求'},
                         'tags': {'label':'关键字'},
                         'cities': {'label':'工作城市'},
                         'salary_range': {'label':'薪资范围'},
                         'company': {'label':'公司'}
                        },
                     )






class AddJobForm(JobForm):


    submit = SubmitField('提交')

    def addjob(self):
        job = Job(name=self.name.data,
                  requirements=self.requirements.data,
                  salary_range=self.salary_range.data,
                  company=self.company.data,
                  tags=self.tags.data,
                  cities=self.cities.data)
        db.session.add(job)
        db.session.commit()

    def updatejob(self, job):
        self.populate_obj(job)   # 从表单中获取最新数据并填充到对象job
        db.session.add(job)
        db.session.commit()


class AddJobForm(JobForm):

    submit = SubmitField('提交')

    def addjob(self):
        job = Job(name=self.name.data,
                  requirements=self.requirements.data,
                  salary_range=self.salary_range.data,
                  company=self.company.data,
                  tags=self.tags.data,
                  cities=self.cities.data)
        db.session.add(job)
        db.session.commit()

    def updatejob(self, job):
        self.populate_obj(job)   # 从表单中获取最新数据并填充到对象job
        db.session.add(job)
        db.session.commit()
