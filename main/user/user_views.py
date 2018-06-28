from flask import Blueprint, Flask, request, json, jsonify, make_response
import jwt
import datetime
import sys, os
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from
from functools import wraps
from ..app_models import db, User, BlackListToken
import re
from flask_cors import CORS

userBlueprint = Blueprint('user', __name__)
CORS(userBlueprint)
SECRET_KEY = 'password reversed drowssap' # secret key
logged_in_user ={}

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
            data = jwt.decode(token,SECRET_KEY)
            # current_user = User.query.get(int(data['id']))
        except:
            return jsonify({'message', 'Token is invalid'}), 401
        return f(*args, **kwargs)

    return decorated


@userBlueprint.route('/api/auth/register', methods=['POST'])
@swag_from('apidocs/create_user.yml')
def create_user():
    jsn = request.data
    data = json.loads(jsn)

    specialChars = ['@', '#', '$', '%', '^', '&', '*', '!', '/', '?', '-', '_']
    
    # check that username is not missing
    if 'username' not in data.keys():
        return jsonify({'message':'username is missing'}), 400 #bad request
    else:
        if len(data['username']) == 0:
            return jsonify({'message':'username is blank'}), 400 #bad request
        #check length of username, should be five characters and above
        if len(data['username']) < 5:
            return jsonify({'message':'username too short, should be between five and ten characters'}), 400 #bad request

        if len(data['username']) > 10:
            return jsonify({'message':'username too long, should be between five and ten characters'}), 400 #bad request
            
        #check whether username contains special characters, its forbidden!
        for x in data['username']:
            if x in specialChars:
                return jsonify({'message':'username contains special characters'}), 400 #bad request

    #check that email is not missing
    if 'email' not in data.keys():
        return jsonify({'message':'email is missing'}), 400 #bad request
    else:
        if len(data['email']) == 0:
            return jsonify({'message':'email is blank'}), 400 #bad request
        #check that the email is in good format
        if not re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[com|org|edu]{3}$)", data['email']):
            return jsonify({'message':'email is not in valid format'}), 400 #bad request

    #check that password is not missing
    if 'password' not in data.keys():
        return jsonify({'message':'password is missing'}), 400 #bad request
    else:
        if len(data['password']) < 5:
            return jsonify({'message':'password too short, should be between five and ten characters'}), 400 #bad request

        # if len(data['password']) > 10:
        #     return jsonify({'message':'password too long, should be between five and ten characters'}), 400 #bad request

    username = data['username']
    password = data['password']
    email = data['email']
       
    if User.query.filter_by(username=username).count() == 0:
        user = User(username=username, password=generate_password_hash(password), email=email)
        if user:
            db.session.add(user)
            db.session.commit()
            return jsonify({'message':'user successfully registered'}), 201 #created
    else:
        return jsonify({'message':'user already exists'}), 400 #bad request


@userBlueprint.route('/api/auth/login', methods=['POST'])
@swag_from('apidocs/user_login.yml')
def login():
    global logged_in_user
    jsn = request.data
    data = json.loads(jsn)
    
    # if logged_in_user:
    #     # username = logged_in_user['username']
    #     return jsonify({'message':'you are already logged in'}), 400

    if data:
        if 'username' not in data.keys():
            return jsonify({"message":"username missing"}), 400

        if 'password' not in data.keys():
            return jsonify({"message":"password missing"}), 400

        un=data['username']
        pd=data['password']
        
        user = User.query.filter_by(username=un).first()
        if not user:
            return jsonify({'message':'wrong username or password or user not registered'}), 400
        
        if check_password_hash(user.password, pd):
            # create the token
            token = jwt.encode({'user':un, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30), 'id':user.id}, SECRET_KEY)
            logged_in_user['id']=user.id
            logged_in_user['username'] = user.username
            logged_in_user['password'] = user.password
            return jsonify({'token':token.decode('UTF-8'), 'message':'successfully logged in'}), 200
        
    return make_response(jsonify({'message':'wrong username or password'})), 400
       

@userBlueprint.route('/api/auth/reset-password', methods=['PUT'])
@swag_from('apidocs/reset_user_password.yml')
@token_required
def reset_password():
    global logged_in_user
    jsn = request.data
    data = json.loads(jsn)

    # if 'username' not in data.keys():
    #     return jsonify({"message":"username missing"})
    
    if 'password' not in data.keys():
        return jsonify({"message":"password missing"})

    if not logged_in_user:
        return jsonify({"message":"please login"})

    if data['password'] != '':
        newPassword = data['password']
        user = User.query.get(logged_in_user['id'])
        user.password= generate_password_hash(newPassword)
        db.session.add(user)
        return jsonify({'message':'user password has been successfully reset'})
    else:
        return jsonify({'message': 'Could not reset password because of missing fields'})


@userBlueprint.route('/api/auth/logout', methods=['POST'])
@token_required
@swag_from('apidocs/user_logout.yml')
def logout():
    auth_token = request.headers.get('x-access-token')
    
    if auth_token:
        print(auth_token)
        res = BlackListToken(auth_token)
        blacklist_token = BlackListToken(token=auth_token)
        # blacklist_token.save(auth_token)
        db.session.add(auth_token)
        db.session.commit()

        # try:
        #     blacklist_token.save(auth_token)
        #     response_object = {
        #         'status': 'success',
        #         'message': 'successfully logged out'
        #     }
        #     return make_response(jsonify(response_object)), 200
        # except Exception as e:
        #     response_object = {
        #         'status': 'failed from thrown exception',
        #         'message': str(e)
        #     }
        #     return make_response(jsonify(response_object)), 200
    else:
        response_object = {
            'status': 'fail from token',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(response_object)), 403
