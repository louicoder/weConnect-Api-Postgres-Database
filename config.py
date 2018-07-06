import os
basedir = os.path.abspath(os.path.dirname(__file__))
from main import app

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'veryHardtoGEtPassword' or os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres@localhost/weconnectdb')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    DEBUG=True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

class ProductionConfig(Config):
    DEBUG = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': TestingConfig
}