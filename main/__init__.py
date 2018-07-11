
import flask
from flask import Flask, redirect
from .user.user_views import userBlueprint
from .business.business_views import businessBlueprint
from .reviews.review_views import reviewBlueprint
from flasgger import Swagger
from flasgger import swag_from
from .app_models import db, Business, User, Review
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.register_blueprint(userBlueprint)
app.register_blueprint(businessBlueprint)
app.register_blueprint(reviewBlueprint)

#create the swagger template
template = {
    "swagger": "2.0",
    "info": {
        "title":
        "We-connect API with postgres database",
        "description":
        "WeConnect provides a platform that brings businesses and individuals together. This platform creates awareness for businesses and gives the users the ability to write reviews about the businesses they have interacted with.", "version":"1.0.0"},
    "schemes": ["http", "https"],
    "specs_route":"/apidocs/"
}

#swagger docs instanciation
swagger = Swagger(app, template=template)
# CORS(app, resources={r"/api/*": {"origins": "*","Access-Control-Allow-Origin":"*","Access-Control-Request-Headers":"*"}})
CORS(app)

@app.route('/')
def index():
    return redirect('/apidocs/')