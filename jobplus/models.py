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

class Job(Base):
    __tablename__ = "job"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False)
    