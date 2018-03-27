import os

class Config:
    """Common configurations"""    
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
   

class DevelopmentConfig(Config):
    """Development configurations"""
    DEBUG = True
    DEVELOPMENT = True


class ProductionConfig(Config):
    """Production configurations"""
    DEBUG= False   
    TESTING = False

class TestingConfig(Config):
    """Testing Configurations"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = 'password reversed drowssap'

    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}