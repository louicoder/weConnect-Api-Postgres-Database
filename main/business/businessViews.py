from flask import Blueprint, Flask, request, json, jsonify, make_response
import jwt
import datetime
from user.userViews import token_required
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from
import sys

sys.path.append('..')
businessBlueprint = Blueprint('business', __name__)

@businessBlueprint.route('/api/businesses', methods=['POST'])
@swag_from('createBusiness.yml')
# @token_required
def createBusiness():
   pass


@businessBlueprint.route('/api/businesses/<string:id>', methods=['GET'])
@swag_from('retrieveBusiness.yml')
# @token_required
def getOneBusiness(id):
    pass
    


@businessBlueprint.route('/api/businesses', methods=['GET'])
@swag_from('retrieveAllBusinesses.yml')
# @token_required
def getAllBusinesses():
    pass


# @businessBlueprint.route('/api/businesses/<string:id>', methods=['PUT'])
# @swag_from('updateBusiness.yml')
# # @token_required
# def updatebusiness(id):
#     pass

        
@businessBlueprint.route('/api/businesses/<string:id>', methods=['DELETE'])
@swag_from('deleteBusiness.yml')
# @token_required
def deletebusiness(id):
    pass


@businessBlueprint.route('/api/businesses/search', methods=['GET'])
@swag_from('searchBusiness.yml')
# @token_required
def searchBusiness():
    pass


@businessBlueprint.route('/api/businesses/filter', methods=['GET'])
@swag_from('filterBusiness.yml')
# @token_required
def filterBusiness():
    pass