from flask import Blueprint, Flask, request, json, jsonify, make_response
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from

userBlueprint = Blueprint('user', __name__)


@userBlueprint.route('/api/auth/register', methods=['POST'])
@swag_from('../swagger/createUser.yml')
def createuser():

    return jsonify({'message':'this is the register route'})
    

@userBlueprint.route('/api/v1/auth/login', methods=['POST'])
def login():
    pass
    

@userBlueprint.route('/api/v1/auth/resetpassword', methods=['POST'])
# @token_required
def resetPassword():
    pass

@userBlueprint.route('/api/v1/auth/logout', methods=['PUT'])
# @token_required
def logout():    
    pass




