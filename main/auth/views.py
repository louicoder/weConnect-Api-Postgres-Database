from functools import wraps
from flask import Response, request, jsonify, make_response
from jwt import 
from ...run import app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        data =''
        if not token:
            return jsonify({'message':'token is missing!'}), 403
        try:
            data = jwt.decode(token, )
        except:
            return make_response(jsonify({'message':'Token is invalid'})), 403

        return f(*args, **kwargs)
    return decorated