import os
import unittest

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
import sys

from main.app_models import User, Business, Review
from run import app
from main.app_models import db
from config import config
from flask_uploads import UploadSet, configure_uploads, IMAGES


db.init_app(app)

# set the image upload directory
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = '/images'
configure_uploads(app, photos)

if(os.environ.get('APP_SETTINGS')=='testing'):
    app.config.from_object(config['testing'])
elif(os.environ.get('APP_SETTINGS')=='production'):
    app.config.from_object(config['production'])
else:
    app.config.from_object(config['development'])

migrate = Migrate(app, db)
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Business=Business, Review=Review)

@manager.command
def migrator():
    os.system('export FLASK_APP=run.py')        
    os.system('flask db init')

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