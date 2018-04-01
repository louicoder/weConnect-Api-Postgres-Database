from flask import Blueprint, Flask, request, json, jsonify, make_response
import random
import jwt
import datetime
import sys
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from

sys.path.append('..')
# from ..authourization.auth import token_required
# from ..run import userBlueprint

userBlueprint = Blueprint('user', __name__)

@userBlueprint.route('/api/auth/register', methods=['POST'])
@swag_from('createUser.yml')
def createuser():
    return jsonify({'message':'just testing'})
        

# @userBlueprint.route('/api/auth/login', methods=['POST'])
# @swag_from('..swagger/loginUser.yml')
# def login():
#     pass
    

# @userBlueprint.route('/api/v1/auth/resetpassword', methods=['POST'])
# @swag_from('..swagger/resetUserPassword.yml')
# # @token_required
# def resetPassword():
#     pass

# @userBlueprint.route('/api/v1/auth/logout', methods=['PUT'])
# @swag_from('userSwagDocs/logoutUser.yml')
# # @token_required
# def logout():    
#     pass




