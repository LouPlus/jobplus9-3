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
        return self._password

    @password.setter
    def password(self, ori_password):
        self._password = generate_password_hash(ori_password)

    def check_password(self,password):
        return check_password_hash(self._password,password)

    @property
    def is_company(self):
        return self.role == ROLE_COMPANY

    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN

class Job(Base):
    __tablename__ = "job"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)
