from flask import Flask
from main.user.userViews import userBlueprint
from main.business.businessViews import businessBlueprint
from main.reviews.reviewViews import reviewBlueprint
from flasgger import Swagger
from config import Config
from appModels import db

app = Flask(__name__)
swagger = Swagger(app)

#lets set the configurations from the config.py file
app.config.from_object(Config)

# db.init_app(app)

#Registering the blueprints for the different views
app.register_blueprint(userBlueprint)
app.register_blueprint(businessBlueprint)
app.register_blueprint(reviewBlueprint)


if __name__ == '__main__':
    app.run(debug=True)