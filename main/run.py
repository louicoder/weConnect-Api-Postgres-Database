from flask import Flask, Blueprint
# from config import Config, config
from appModels import db
from flasgger import Swagger
from flasgger import swag_from
import sys
from user.userViews import userBlueprint

# userBlueprint = Blueprint('user', __name__)
# businessBlueprint = Blueprint('business', __name__)
# reviewBlueprint = Blueprint('review', __name__)

app = Flask(__name__)
swagger = Swagger(app)

#Registering the blueprints for the different views
app.register_blueprint(userBlueprint)
# app.register_blueprint(businessBlueprint)
# app.register_blueprint(reviewBlueprint)



#lets set the configurations from the config.py file
# app.config.from_object(Config)
# app.config['SQLALCHEMY_DATABASE_URI'] =

# db.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)