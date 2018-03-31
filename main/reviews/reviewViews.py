from flask import Blueprint, Flask, request, json, jsonify, make_response
from ..authourization.auth import token_required
from flasgger import swag_from

reviewBlueprint = Blueprint('reviews', __name__)


@reviewBlueprint.route('/api/businesses/<string:id>/reviews', methods=['POST'])
@swag_from('../swaggerDocs/reviewSwagDocs/createReview.yml')
@token_required
def createReview(id):
    pass


@reviewBlueprint.route('/api/businesses/<string:id>/reviews', methods=['POST'])
@swag_from('../swaggerDocs/reviewSwagDocs/createReview.yml')
@token_required
def getAllReviews(id):
    pass