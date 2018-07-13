import os
basedir = os.path.abspath(os.path.dirname(__file__))
from main import app

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'veryHardtoGEtPassword' or os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres@localhost/weconnectdb')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # SQLALCHEMY_DATABASE_URI = "postgres://olcnxvexiyysit:b3c5c2b84737b398a8c77e4dd7caca9466f6defb217c840755024cae5d151e3b@ec2-23-21-236-249.compute-1.amazonaws.com:5432/dbp41ulsu8stu7"

    
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': TestingConfig
}