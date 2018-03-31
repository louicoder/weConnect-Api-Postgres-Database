import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
import sys


sys.path.append('..')
from appModels import User
from appModels import Business
from appModels import Review
from config import Config

from run import app
from appModels import db

db.init_app(app)
app.config.from_object(Config)
app.config[]

migrate = Migrate(app, db)
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Business=Business, Review=Review)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()