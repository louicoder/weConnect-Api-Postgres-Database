# import os
# basedir = os.path.abspath(os.path.dirname(__file__))

# class Config:
#     """Common configurations"""
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'password reversed drowssap'
#     SQLALCHEMY_COMMIT_ON_TEARDOWN = True
#     SQLALCHEMY_TRACK_MODIFICATIONS = True
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

#     @staticmethod
#     def init_app(app):
#         pass
   

# class DevelopmentConfig(Config):
#     """Development configurations"""
#     DEBUG = True
#     DEVELOPMENT = True
#     DATABASE_URL = 'sqlite:///' + os.path.join(basedir, 'testdb.sqlite')
#     # DATABASE_URL = 'sqlite:///db.sqlite'
#     SECRET_KEY = 'password reversed drowssap'
    

# class ProductionConfig(Config):
#     """Production configurations"""
#     DEBUG= False   
#     TESTING = False

# class TestingConfig(Config):
#     """Testing Configurations"""
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    

    
# config = {
#     'development': DevelopmentConfig,
#     'testing': TestingConfig,
#     'production': ProductionConfig,
#     'default': DevelopmentConfig
# }