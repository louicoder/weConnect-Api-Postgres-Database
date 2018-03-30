import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Common configurations"""    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'password reversed drowssap'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
   

class DevelopmentConfig(Config):
    """Development configurations"""
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTDB') or 'sqlite:////' + os.path.join(basedir, 'testdb.sqlite')
    SECRET_KEY = 'password reversed drowssap'
    

class ProductionConfig(Config):
    """Production configurations"""
    DEBUG= False   
    TESTING = False

class TestingConfig(Config):
    """Testing Configurations"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    

    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}