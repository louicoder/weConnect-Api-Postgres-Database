from flask import Blueprint
from flask import Blueprint, Flask, request, json, jsonify, make_response


reviewBlueprint = Blueprint('reviews', __name__)


@reviewBlueprint.route('/api/businesses/<string:id>/reviews', methods=['POST'])
def createReview(id):
    pass