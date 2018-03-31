from flask import Blueprint, Flask, request, json, jsonify, make_response
import jwt
import datetime
from ..authourization.auth import token_required
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from

userBlueprint = Blueprint('user', __name__)


@userBlueprint.route('/api/auth/register', methods=['POST'])
@swag_from('../swaggerDocs/userSwagDocs/createUser.yml')
def createuser():
    pass
        

@userBlueprint.route('/api/auth/login', methods=['POST'])
@swag_from('../swaggerDocs/userSwagDocs/loginUser.yml')
def login():
    pass
    

@userBlueprint.route('/api/v1/auth/resetpassword', methods=['POST'])
@swag_from('../swaggerDocs/userSwagDocs/resetUserPassword.yml')
@token_required
def resetPassword():
    pass

@userBlueprint.route('/api/v1/auth/logout', methods=['PUT'])
@swag_from('../swaggerDocs/userSwagDocs/logoutUser.yml')
@token_required
def logout():    
    pass




