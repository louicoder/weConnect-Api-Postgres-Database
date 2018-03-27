from flask import Blueprint, Flask, request, json, jsonify, make_response
from .userModel import User, USERS
import jwt
import datetime
from functools import wraps
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

loggedInUser=[]
userBlueprint = Blueprint('user', __name__)

SECRETKEY = 'thisISverysecret'
token = None

@userBlueprint.route('/api/v1/auth/register', methods=['POST'])
def createuser():
    pass
    

@userBlueprint.route('/api/v1/auth/getusers', methods=['GET'])
@token_required
def getusers():
    pass
    

@userBlueprint.route('/api/v1/auth/login', methods=['POST'])
def login():
    pass
    

@userBlueprint.route('/api/v1/auth/resetpassword', methods=['POST'])
@token_required
def resetPassword():
    pass

@userBlueprint.route('/api/v1/auth/logout', methods=['PUT'])
@token_required
def logout():    
    pass




