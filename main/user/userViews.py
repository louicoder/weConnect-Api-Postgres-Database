from flask import Blueprint, Flask, request, json, jsonify, make_response
import jwt
import datetime
import sys, os
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from
from functools import wraps
from ..appModels import db, User, BlackList, BlackList

# from run import SECRET_KEY

# sys.path.append('..')
# from run import app

userBlueprint = Blueprint('user', __name__)
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
            current_user = User.query.get(int(data['id']))
        except:
            return jsonify({'message', 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)

    return decorated


@userBlueprint.route('/api/auth/register', methods=['POST'])
@swag_from('createUser.yml')
def create_user():
    jsn = request.data
    data = json.loads(jsn)
    username = data['username']
    password = data['password']
    email = data['email']

    specialChars = ['@', '#', '$', '%', '^', '&', '*', '!', '/', '?', '-', '_']
    
    # check that username is not missing
    if 'username' not in data.keys():
        return jsonify({'message':'username is missing'}), 400 #bad request
    else:
        username = data['username']

    #check that email is not missing
    if 'email' not in data.keys():
        return jsonify({'message':'email is missing'}), 400 #bad request
    else:
        email = data['email']

    #check that password is not missing
    if 'password' not in data.keys():
        return jsonify({'message':'password is missing'}), 400 #bad request
    else:
        password = data['password']

    #check whether username contains special characters, its forbidden!
    for x in username:
        if x in specialChars:
            return jsonify({'message':'username contains special characters'}), 400 #bad request

    #check length of username, should be five characters and above
    if len(username) < 5:
        return jsonify({'message':'username too short, should be five characters and above'}), 400 #bad request

    if len(username) > 10:
        return jsonify({'message':'username too long, should be five characters and above'}), 400 #bad request

    if len(data['password']) < 5:
        return jsonify({'message':'password too short, should be between five and ten characters'}), 400 #bad request

    if len(data['password']) > 10:
        return jsonify({'message':'password too long, should be between five and ten characters'}), 400 #bad request

    #check if the email contains a dot
    if '.' not in data['email']:
        return jsonify({'message':'email is invalid, dot missing'}), 400 #bad request

    #check if the email contains an @ symbol
    if '@' not in data['email']:
        return jsonify({'message':'email is invalid, @ symbol missing'}), 400 #bad request

    if not username or not password or not email:
        return jsonify({'message':'make sure that you have passed all fields.'})
    else:        
        if User.query.filter_by(username=username).count() == 0:
            user = User(username=username, password=generate_password_hash(password), email=email)
            if user:
                db.session.add(user)
                db.session.commit()
                return jsonify({'message':'user successfully registered'}), 201 #created
        else:
            return jsonify({'message':'user already exists'}), 400 #bad request
        password

@userBlueprint.route('/api/auth/login', methods=['POST'])
@swag_from('loginUser.yml')
def login():
    global logged_in_user
    auth = None   
    jsn = request.data
    data = json.loads(jsn)

    if logged_in_user:
        username = logged_in_user['username']
        return jsonify({'message':'already logged in as '+username})

    if auth:
        un=auth.username
        pd=auth.password

        #if no password is given.
        if not un:
            return jsonify({"message":"no username was provided"}), 400

        #if no password is given.
        if not pd:
            return jsonify({"message":"no password was provided"}), 400

        token = jwt.encode({'user':auth.username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, SECRET_KEY)
        print(token)
        user = User.query.filter_by(username=un).first()
        print(user)
        if check_password_hash(user.password, pd):
            logged_in_user['id']=user.id
            logged_in_user['username'] = user.username
            logged_in_user['password'] = user.password
            return jsonify({'token':token.decode('UTF-8'), 'message':'successfully logged in'}), 200
    elif data:

        un=data['username']
        pd=data['password']


        token = jwt.encode({'user':un, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, SECRET_KEY)
        print(token)
        user = User.query.filter_by(username=un).first()
        print(user)
        if check_password_hash(user.password, pd):
            logged_in_user['id']=user.id
            logged_in_user['username'] = user.username
            logged_in_user['password'] = user.password
            return jsonify({'token':token.decode('UTF-8'), 'message':'successfully logged in'}), 200
    else:
        return make_response(jsonify({'message':'wrong username or password'})), 404
        
    return make_response(jsonify({'message':'wrong username or password'})), 401
       

@userBlueprint.route('/api/auth/reset-password', methods=['PUT'])
@swag_from('resetUserPassword.yml')
@token_required
def reset_password():
    global logged_in_user
    jsn = request.data
    data = json.loads(jsn)
    
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
@swag_from('logoutUser.yml')
# @token_required
def logout():    
    # 
    global logged_in_user
    if not logged_in_user:
        return jsonify({"message":"you are already logged out"}), 400
    # tk = request.headers['x-access-token'
    
    # token = BlackList(token=tk)
    # db.session.add(token)
    # db.session.commit()
    
    # if BlackList.query.filter_by(token=token).count() == 1:
    return jsonify({"message":"successfully logged out"})






