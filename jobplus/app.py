from flask import Flask
from jobplus.config import configs
from jobplus.models import db

from flask_moment import Moment

def register_extentions(app):
    db.init_app(app)
    Moment(app)

def register_blueprints(app):
    from .handlers import front, job
    app.register_blueprint(front)
    app.register_blueprint(job)

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    
    register_extentions(app)
    register_blueprints(app)
    
    return app
