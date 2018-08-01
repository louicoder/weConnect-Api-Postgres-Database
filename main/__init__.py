
import flask
from flask import Flask, redirect
from .user.user_views import userBlueprint
from .business.business_views import businessBlueprint
from .reviews.review_views import reviewBlueprint
from flasgger import Swagger
from flasgger import swag_from
from .app_models import db, Business, User, Review
from flask_cors import CORS, cross_origin

from flask_uploads import UploadSet, configure_uploads, IMAGES


app = Flask(__name__,static_url_path='/images')
app.register_blueprint(userBlueprint)
app.register_blueprint(businessBlueprint)
app.register_blueprint(reviewBlueprint)

# URL for connecting to the application. first is localhost, second is for connecting to heroku
# BASE_URL = 'http://127.0.0.1:5000' # for local host

# BASE_URL = 'https://weconnect-api-app.herokuapp.com' #for heroku application

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
# initialise app
# db.init_app(app)


#swagger docs instanciation
swagger = Swagger(app, template=template)
CORS(app)

@app.route('/')
def index():
    return redirect('/apidocs/')