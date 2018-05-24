
import flask
from flask import Flask, redirect
from .user.userViews import userBlueprint
from .business.businessViews import businessBlueprint
from .reviews.reviewViews import reviewBlueprint
from flasgger import Swagger
from flasgger import swag_from
from .appModels import db, Business, User, Review


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

@app.route('/')
def index():
    return redirect('/apidocs/')