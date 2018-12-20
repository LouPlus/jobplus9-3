from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime 
db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(Base):
    __tablename__ = "user"

    ROLE_ADMIN = 10
    ROLE_COMPANY = 20
    ROLE_JOBHUNTER = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)

    


class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    jobs = db.relationship('Job')

    def __repr__(self):
        return '<Company:{}>'.format(self.name)


job_tag = db.Table('job_tag',
                   db.Column('job_id', db.Integer, db.ForeignKey('job.id'), primary_key=True),
                   db.Column('tag_id', db.Integer, db.ForeignKey('jtag.id'), primary_key=True))



job_city = db.Table('job_city',
                   db.Column('job_id', db.Integer, db.ForeignKey('job.id'), primary_key=True),
                   db.Column('city_id', db.Integer, db.ForeignKey('jcity.id'), primary_key=True))



class Jtag(Base):
    __tablename__ = 'jtag'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, index=True, nullable=False)

    def __repr__(self):
        return '<Jtag:{}>'.format(self.name)




class Jcity(Base):
    __tablename__ = 'jcity'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, index=True, nullable=False)

    def __repr__(self):
        return '<Jcity:{}>'.format(self.name)




class Salary_Range(Base):
    __tablename__ =  'salary_range'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    left = db.Column(db.Integer)
    right = db.Column(db.Integer)
    jobs = db.relationship('Job')


    def __repr__(self):
        return '{}元 -- {}元'.format(self.left, self.right)

    __str__ = __repr__




class Job(Base):
    __tablename__ = "job"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)
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
