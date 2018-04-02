from flask import Blueprint, Flask, request, json, jsonify, make_response
import jwt
import sys, os
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from
from functools import wraps


sys.path.append('')
from appModels import User
from business.businessViews import businessBlueprint

userBlueprint = Blueprint('user', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        """checks whether token is valid or not."""
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        else:
            return jsonify({'message':'Token not valid'}), 401

        if not token:
            return jsonify({'message ':'Unauthorized access token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.get(int(data['id']))
        except:
            return jsonify({'message', 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)

    return decorated

@userBlueprint.route('/api/auth/register', methods=['POST'])
@swag_from('createUser.yml')
def createUser():
    return jsonify({'message':'just testing'})
        

@userBlueprint.route('/api/auth/login', methods=['POST'])
@swag_from('loginUser.yml')
def login():
    pass
    

@userBlueprint.route('/api/v1/auth/resetpassword', methods=['PUT'])
@swag_from('resetUserPassword.yml')
# @token_required
def resetPassword():
    pass

@userBlueprint.route('/api/v1/auth/logout', methods=['POST'])
@swag_from('logoutUser.yml')
# @token_required
def logout():    
    pass




