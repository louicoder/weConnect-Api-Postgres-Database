import os
import unittest

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
import sys

from main.appModels import User
from main.appModels import Business
from main.appModels import Review
from run import app
from main.appModels import db


db.init_app(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI']= os.environ.get('DATABASE_URL')
app.config['DEBUG'] = os.getenv('DEBUG')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

migrate = Migrate(app, db)
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Business=Business, Review=Review)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@app.cli.command()
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()