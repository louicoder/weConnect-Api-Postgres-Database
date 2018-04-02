from functools import wraps
from flask import Response, request, jsonify, make_response
import jwt
import sys

sys.path.append('')
from ..appModels import User
from run import token_required, app

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