from flask import Blueprint, Flask, request, json, jsonify, make_response
import jwt
import sys
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from
from functools import wraps

sys.path.append('')
from appModels import User


userBlueprint = Blueprint('user', __name__)


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




