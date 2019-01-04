import os
class BaseConfig:
    """ 配置基类 """
    SECRET_KEY='codeofteam9-3'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JOBINDEX_PER_PAGE = 9


    ADMIN_PER_PAGE = 12

class DevelopmentConfig(BaseConfig):
    """ 开发环境配置 """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root@localhost:3306/jobplus?charset=utf8"
    #SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost:3306/jobplus?charset=utf8"

class ProductionConfig(BaseConfig):
    """ 生产环境配置 """
    pass

class TestingConfig(BaseConfig):
    """ 测试环境配置 """
    pass

class Esun127Config(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@192.168.0.209:3306/jobplus?charset=utf8"

configs = {
    'development' : DevelopmentConfig,
    'production' : ProductionConfig,
    'testing' : TestingConfig,
    'esun127' : Esun127Config,
}
