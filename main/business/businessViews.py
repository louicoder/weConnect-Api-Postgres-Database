from flask import Blueprint, Flask, request, json, jsonify, make_response
import jwt
import datetime
from ..authourization.auth import token_required
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from
import sys

sys.path.append('..')
from ..run import businessBlueprint
# businessBlueprint = Blueprint('business', __name__)

@businessBlueprint.route('/api/businesses', methods=['POST'])
@swag_from('../swaggerDocs/businessSwagDocs/createBusiness.yml')
@token_required
def createBusiness():
   pass


@businessBlueprint.route('/api/businesses/<string:id>', methods=['GET'])
@swag_from('../swaggerDocs/businessSwagDocs/retrieveBusiness.yml')
@token_required
def getOneBusiness(id):
    pass
    


@businessBlueprint.route('/api/businesses', methods=['GET'])
@swag_from('../swaggerDocs/businessSwagDocs/retrieveAllBusiness.yml')
@token_required
def getAllBusinesses():
    pass


@businessBlueprint.route('/api/businesses/<string:id>', methods=['PUT'])
@swag_from('../swaggerDocs/businessSwagDocs/updateBusiness.yml')
@token_required
def updatebusiness(id):
    pass

        
@businessBlueprint.route('/api/businesses/<string:id>', methods=['DELETE'])
@swag_from('../swaggerDocs/businessSwagDocs/deleteBusiness.yml')
@token_required
def deletebusiness(id):
    pass