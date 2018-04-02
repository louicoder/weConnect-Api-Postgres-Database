from flask import Blueprint, Flask, request, json, jsonify, make_response
# from ...authourization.auth import token_required
from flasgger import swag_from
from user.userViews import token_required
import sys


reviewBlueprint = Blueprint('reviews', __name__)
@reviewBlueprint.route('/api/businesses/<string:id>/reviews', methods=['POST'])
@swag_from('createReview.yml')
# @token_required
def createReview(id):
    pass


@reviewBlueprint.route('/api/businesses/<string:id>/reviews', methods=['GET'])
@swag_from('retrieveReviews.yml')
# @token_required
def getAllReviews(id):
    pass