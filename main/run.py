from flask import Flask, Blueprint
# from config import Config, config
from appModels import db
from flasgger import Swagger
from flasgger import swag_from
import sys, os
from user.userViews import userBlueprint
from business.businessViews import businessBlueprint
from reviews.reviewViews import reviewBlueprint

app = Flask(__name__)
swagger = Swagger(app)

#Registering the blueprints for the different views
app.register_blueprint(userBlueprint)
app.register_blueprint(businessBlueprint)
app.register_blueprint(reviewBlueprint)

db.init_app(app)

# testing
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'testdb.sqlite')
app.config['DEBUG'] = True

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# app.config['SECRET_KEY'] = 'password reversed drowssap'



if __name__ == '__main__':
    app.run(debug=True)