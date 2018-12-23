from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base, UserMixin):
    __tablename__ = "user"

    ROLE_ADMIN = 10
    ROLE_COMPANY = 20
    ROLE_JOBHUNTER = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_JOBHUNTER)

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        """Python 风格的 getter """
        return self._password

    @password.setter
    def password(self, ori_password):
        """ Python 风格的 setter, 这样设置 user.password 就会自动为 password 生成哈希制存入 _password 字段 """
        self._password = generate_password_hash(ori_password)

    def check_password(self,password):
        """ 判断用户输入的密码和存储的 hash 密码是否相等 """
        return check_password_hash(self._password,password)


    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN




class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    website = db.Column(db.String(64), unique=True)
    # 公司简介
    profile = db.Column(db.String(128))
    # 公司详细介绍
    description = db.Column(db.String(512))
    # Logo图片 url 地址
    url = db.Column(db.String(128), default="https://pic.baike.soso.com/ugc/baikepic2/18723/20180202144851-1145158508_jpg_462_344_6048.jpg/0")
    address = db.Column(db.String(64), nullable=False)
    jobs = db.relationship('Job')

    def __repr__(self):
        return '<Company:{}>'.format(self.name)


job_tag = db.Table('job_tag',
                   db.Column('job_id', db.Integer, db.ForeignKey('job.id'), primary_key=True),
                   db.Column('tag_id', db.Integer, db.ForeignKey('jtag.id'), primary_key=True))



job_city = db.Table('job_city',
                   db.Column('job_id', db.Integer, db.ForeignKey('job.id'), primary_key=True),
                   db.Column('city_id', db.Integer, db.ForeignKey('jcity.id'), primary_key=True))



class Jtag(db.Model):
    __tablename__ = 'jtag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, index=True, nullable=False)

    def __repr__(self):
        return '{}'.format(self.name)




class Jcity(db.Model):
    __tablename__ = 'jcity'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, index=True, nullable=False)

    def __repr__(self):
        return '{}'.format(self.name)




class Salary_Range(db.Model):
    __tablename__ =  'salary_range'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    jobs = db.relationship('Job')


    def __repr__(self):
       return '--'.join([x+'元' for x in self.name.split('--')])

    __str__ = __repr__




class Job(Base):
    __tablename__ = "job"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    requirements = db.Column(db.String(1024))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete="CASCADE"))
    salary_range_id = db.Column(db.Integer, db.ForeignKey('salary_range.id',ondelete="SET NULL"))
    salary_range = db.relationship('Salary_Range', uselist=False)
    company = db.relationship('Company', uselist=False)
    # 增加反向引用,使得Job对象增加tags属性的同时, Jtag对象增加jobs属性
    tags = db.relationship('Jtag', secondary=job_tag, backref=db.backref('jobs'))
    cities = db.relationship('Jcity', secondary=job_city, backref=db.backref('jobs'))


    def __repr__(self):
        return "<Job:{}>".format(self.name)



