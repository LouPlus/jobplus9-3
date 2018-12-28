from flask import url_for, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField


from wtforms.fields import SelectField

from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError
from flask_wtf.file import FileField


from jobplus.models import db, User, Job , Company,  HunterProfile, Resume
from jobplus.models import Jtag, Jcity, Salary_Range

from werkzeug.utils import secure_filename
from wtforms.ext.sqlalchemy.orm import model_form


import re
import os
import time

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

    def create_user(self, register_role):
        user = User(
            username=self.username.data,
            email=self.email.data,
            password=self.password.data,
            role=register_role
        )

        # 如果是求职者, 则注册时也同时创建它的profile
        if register_role == 30:
            user.profile = HunterProfile(name=user.username, email=user.email)
            user.profile.set_password_fromuser(user)
            db.session.add(user.profile)

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
    name = StringField("公司名称", validators=[DataRequired()])
    email = StringField("邮箱地址", validators=[DataRequired(), Email()])
    phone_number = StringField("公司电话", validators=[DataRequired(), Length(11)])
    address = StringField("公司地址", validators=[DataRequired()])
    website = StringField("公司官网", validators=[DataRequired()])
    logo = StringField("公司LOGO", validators=[DataRequired()])
    description = StringField("公司描述", validators=[DataRequired()])
    info = StringField("公司信息", validators=[DataRequired()])
    submit = SubmitField("提交")

    def update_company(self, user):
        company = Company (name = self.name.data,
            address = self.address.data,
            website = self.website.data,
            url = self.logo.data,
            description = self.description.data,
            user = user)

        db.session.add(company)
        db.session.commit()
        return company


####################  定义求职者配置表单
class HunterProfileForm(FlaskForm):
    name = StringField('姓名')
    email = StringField('邮箱', validators=[Email()])
    password = PasswordField('密码')
    phonenum = StringField('手机号码', validators=[Length(11)])

    workage = SelectField('工作年限', coerce=str,  choices=[
        ('1年', '1年'), ('2年', '2年'), ('3年', '3年'), ('1-3年', '1-3年'),
        ('3-5年', '3-5年'), ('5年以上', '5年以上')], default='2年'
    )
    resume_doc = FileField('上传简历')
    submit = SubmitField('提交')


    def validate_phonenum(self, field):
        reg = re.compile(r'(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\d{8}')
        if not reg.match(field.data):
            raise ValidationError('手机号码格式有误.')


    def createprofile(self, user):
        # 获取用户的profile
        profile = user.profile   # 如果当前用户的profile为空, 则新建profile
        if not profile:
            profile = HunterProfile()

        if self.name.data:
            user.username = self.name.data
        profile.name = user.username

        if self.email.data:
            user.email = self.email.data
        profile.email = user.email

        # 配置表单中密码若有输入,则修改user的密码
        if self.password.data:
            user.password = self.password.data
        profile.set_password_fromuser(user)

        profile.phone_num = self.phonenum.data
        profile.work_age = self.workage.data



        # 处理文件上传
        f = self.resume_doc.data
        if f:
            # 设置简历
            if not profile.resumes:
                profile.resumes = []
            jianlidir = os.path.join(current_app.static_folder, 'jianlis')
            print(f.filename, type(f.filename))
            suffix = secure_filename(f.filename).split('.')[-1]
            #print(filename, type(filename))


            length=len(profile.resumes)+1
            filename = str(time.time())+str(length)+'.'+suffix
            print(filename)
            f.save(os.path.join(jianlidir, filename))
            resume = Resume(
                path=url_for('static', filename='jianlis/'+filename),
                name="{}_{}-resume".format(profile.name,str(length))
            )
            db.session.add(resume)   # 添加简历
            profile.resumes.append(resume)

        user.profile = profile
        db.session.add(profile)
        db.session.add(user)
        db.session.commit()
        return profile




#######################  求职者配置表单结束


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
                     only=['name','requirements', 'tags', 'cities', 'salary_range',
                           'description', 'edulevel', 'experlevel'],
                     field_args =
                     {
                        'name': { 'label':'职位名称', 'validators':[DataRequired(), Length(1, 32)]},
                        'requirements': {'label':'具体要求'},
                         'tags': {'label':'职位标签'},
                         'cities': {'label':'工作城市'},
                         'salary_range': {'label':'薪资范围'},
                         'description': {'label':'职位介绍'},
                         'edulevel': {'label':'学历要求'},
                         'experlevel': {'label':'经验要求'}
                        },
                     )

class AddJobForm(JobForm):
    submit = SubmitField('提交')

    def addjob(self, company):
        job = Job(name=self.name.data,
                  requirements=self.requirements.data,
                  salary_range=self.salary_range.data,
                  description=self.description.data,
                  edulevel=self.edulevel.data,
                  experlevel=self.experlevel.data,
                  tags=self.tags.data,
                  cities=self.cities.data)
        job.company = company

        db.session.add(job)
        db.session.commit()

    def updatejob(self, company, job):
        self.populate_obj(job)   # 从表单中获取最新数据并填充到对象job
        job.company = company
        db.session.add(job)
        db.session.commit()
