class BaseConfig:
    SECRET_KEY='codeofteam9-3'
    SQLALCHEMY_TRACK_MODIFICATIONS=False

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost:3306/jobplus?charset=utf8"

class ProductionConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    pass

class Esun127Config(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@192.168.0.209:3306/jobplus?charset=utf8"

configs = {
    'development' : DevelopmentConfig,
    'production' : ProductionConfig,
    'testing' : TestingConfig,
    'esun127' : Esun127Config,
}
    
