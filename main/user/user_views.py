from flask import Blueprint, Flask, request, json, jsonify, make_response
import jwt
import smtplib
import datetime
from dateutil import relativedelta
import sys, os
import random, string
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from
from functools import wraps
from ..app_models import db, User, BlackListToken, ResetPassword
import re
from flask_cors import CORS
from . import BASE_URL, EMAIL_BASE_URL


userBlueprint = Blueprint('user', __name__)
CORS(userBlueprint)
SECRET_KEY = 'password reversed drowssap' # secret key

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        """checks whether token is valid or not."""
        token = ""
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        else:
            return jsonify({'message':'Token not valid'}), 401

        if not token:
            return jsonify({'message ':'Unauthorized access token is missing'}), 401
        try:
            data = jwt.decode(token,SECRET_KEY)
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
    jsn = request.data
    data = json.loads(jsn)
    
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
            token = jwt.encode({'user':un, 'exp':datetime.datetime.utcnow() + datetime.timedelta(hours=24), 'id':user.id, 'username':user.username}, SECRET_KEY)
            return jsonify({'token':token.decode('UTF-8'), 'message':'successfully logged in'}), 200
        
    return make_response(jsonify({'message':'wrong username or password'})), 400
       

@userBlueprint.route('/api/auth/reset-password', methods=['PUT'])
@swag_from('apidocs/reset_user_password.yml')
@token_required
def reset_password():
    jsn = request.data
    data = json.loads(jsn)
    payload = request.headers.get('x-access-token')
    payload = jwt.decode(payload, SECRET_KEY)
    user_id = payload['id']

    if 'password' not in data.keys():
        return jsonify({"message":"password missing"})

    if data['password'] != '':
        new_password = data['password']
        user = User.query.get(user_id)
        user.password= generate_password_hash(new_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message':'user password has been successfully reset'})
    else:
        return jsonify({'message': 'Could not reset password because of missing fields'})


@userBlueprint.route('/api/auth/reset-password-email/<string:username>', methods=['PUT'])
def update_password_email(username):
    jsn = request.data
    data = json.loads(jsn)
    new_password = generate_password_hash(data['password'])
    secret_code = data['secret_code']
    username = username
    # query database to check whether user exists
    user_object = User.query.filter_by(username=username).first()

    # if user exists
    if user_object:
        reset_password_object = ResetPassword.query.filter_by(username=username).first()
        
        # check if secret code supplied by user is same as one in the database
        if reset_password_object and reset_password_object.secret_code == secret_code:
            difference = relativedelta.relativedelta(datetime.datetime.now(), reset_password_object.reset_time)
            # check if the minutes are not greater than 30 minutes and less than one hour
            if difference.minutes <= 30 and difference.hours < 1:
                user_object.password = new_password
                db.session.add(user_object)
                db.session.commit()
                return jsonify({'message':'password successfully updated'}), 200 #ok ,updated
            else:
                return jsonify({'message':'The secret code has already expired, Try again'}), 400
        else:
            return jsonify({'message':'The secret code you supplied does not match with the one in the records'}), 400
    else:
        return jsonify({'message':'no record for '+username+' was not found, nothing updated'}), 404 # not found

    return jsonify({'message':'password for '+username+' was not updated, try again'}), 400  


@userBlueprint.route('/api/auth/reset-password-email/<string:username>', methods=['POST'])
def reset_password_email(username):
    # query User table to check whether user exists.
    user_object = User.query.filter_by(username=username).first()
    secret_code = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
    
    # if the user exists
    if user_object:
        user_email = user_object.email #set email
        username = username #set username
    else:
        return jsonify({'message': username+' does not exist in the records'}), 400

    try:
        # instantiate gmail server instance
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        # start secure connection.
        server.starttls()
        server.login('musanje2010@gmail.com', os.getenv('PASSWORD'))
        # format the email to include subject, link and secret code
        link = "Click the link below to reset your password  \n "+EMAIL_BASE_URL+"/"+"reset-password-email/"+username+" \n\n Your secret code is:\n"+secret_code
        message = 'Subject: {}\n\n{}'.format('Password reset', link)
        # send email
        server.sendmail('musanje2010@gmail.com', user_email, message)
        server.quit() # close server connection.

        # query database to check whether user with that username exists
        obj = ResetPassword.query.filter_by(username=username).first()
        if obj:          
            # set reset_time to now
            obj.reset_time = datetime.datetime.now()
            obj.secret_code = secret_code
            # save the new time
            db.session.add(obj)
            db.session.commit()
            
        else:
            # this block covers instance where user has no entry in the reset_password table.
            reset_password_object = ResetPassword(username, secret_code)
            db.session.add(reset_password_object)
            db.session.commit()        
        return jsonify({'message':"Email successfully sent to "+ user_email})
    except:
        return jsonify({'message':'Email failed to send'})


@userBlueprint.route('/api/auth/logout', methods=['POST'])
@token_required
@swag_from('apidocs/user_logout.yml')
def logout():
    auth_token = request.headers.get('x-access-token')
    
    if auth_token:
        # res = BlackListToken(auth_token)
        blacklist_token = BlackListToken(token=auth_token)
        # blacklist_token.save(auth_token)
        db.session.add(auth_token)
        db.session.commit()

    else:
        response_object = {
            'status': 'fail from token',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(response_object)), 403
