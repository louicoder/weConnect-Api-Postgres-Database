from flask import Blueprint, Flask, request, json, jsonify, make_response
import jwt
import datetime
import sys, os
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from
from functools import wraps
from appModels import db, User

# from run import SECRET_KEY

# sys.path.append('..')
# from run import app

userBlueprint = Blueprint('user', __name__)
SECRET_KEY = 'password reversed drowssap' # secret key
loggedInUser ={}

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
def createUser():
    jsn = request.data
    data = json.loads(jsn)
    username = data['username']
    password = data['password']
    email = data['email']

    if not username or not password or not email:
        return jsonify({'message':'make sure that you have passed all fields.'})
    else:        
        if User.query.filter_by(username=username).count() == 0:
            user = User(username=username, password=password, email=email)
            if user:
                db.session.add(user)
                db.session.commit()
                return jsonify({'message':'User successfully registered'})
        else:
            return jsonify({'message':'user already exists'})    
        

@userBlueprint.route('/api/auth/login', methods=['POST'])
@swag_from('loginUser.yml')
def login():
    auth = request.authorization
    un=auth.username
    pd=auth.password
    
    if auth:
        token = jwt.encode({'user':auth.username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, SECRET_KEY)
        user = User.query.filter_by(username=un, password=pd).first()
        if user:
            loggedInUser['id']=user.id
            loggedInUser['username']=user.username
            loggedInUser['password']=user.password
            return jsonify({'message': 'username and password correct', 'token':token.decode('UTF-8'), 'id':loggedInUser['id']}), 200
        else:
            return make_response(jsonify({'message':'user doesn''t exist in the system'})), 404

        return jsonify({'token': token.decode('UTF-8')})
    return make_response(jsonify({'message':'couldnt verify'})), 401
       

@userBlueprint.route('/api/auth/reset-password', methods=['PUT'])
@swag_from('resetUserPassword.yml')
# @token_required
def resetPassword():
    global loggedInUser
    jsn = request.data
    data = json.loads(jsn)
    print(loggedInUser)

    if data['password'] != '':
        newPassword = data['password']
        user = User.query.get(loggedInUser['id'])
        user.password= newPassword
        # data['password'] = newPassword
        db.session.add(user)
        
        return jsonify({'message':'user password has been successfully reset'})
    else:
        return jsonify({'message': 'Could not reset password because of missing fields'})
    # return jsonify({'message': 'Could not reset password because of missing fields'})


@userBlueprint.route('/api/v1/auth/logout', methods=['POST'])
@swag_from('logoutUser.yml')
# @token_required
def logout():    
    pass


@userBlueprint.route('/api/auth/getusers', methods=['GET'])
# @token_required
def getusers():    
    users = User.query.all()    
    return jsonify({'message':[user.returnJson() for user in users]})






