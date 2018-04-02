from flask import Flask, Blueprint
# from config import Config, config
from appModels import db
from flasgger import Swagger
from flasgger import swag_from
import sys
from user.userViews import userBlueprint
from business.businessViews import businessBlueprint
from reviews.reviewViews import reviewBlueprint

app = Flask(__name__)
swagger = Swagger(app)

#Registering the blueprints for the different views
app.register_blueprint(userBlueprint)
app.register_blueprint(businessBlueprint)
app.register_blueprint(reviewBlueprint)


if __name__ == '__main__':
    app.run(debug=True)