from flask import Blueprint, Flask, request, json, jsonify, make_response
from flasgger import swag_from
from user.userViews import token_required, loggedInUser
import sys
from appModels import db, Business, Review

reviewBlueprint = Blueprint('reviews', __name__)
@reviewBlueprint.route('/api/businesses/<int:id>/reviews', methods=['POST'])
@swag_from('createReview.yml')
# @token_required
def createReview(id):
    """Function is responsible fof creating a new review"""
    global loggedInUser
    jsn = request.data
    data = json.loads(jsn)
    id = id

    #check whether business exists before creating review
    exists = checkBizExists(id)
    userid= exists.userid
    if exists:
        if 'review' in data.keys():
            review = data['review']
            rev = Review(review, int(userid), exists.id)
            db.session.add(rev)
            db.session.commit()
            return jsonify({'message':'Review has been successfully created', 'review':rev.returnJson()}), 200
        else:
            return jsonify({'message':'missing field "review"'}), 400
    else:
        return jsonify({'message':'No business with that id exists'}), 404


def checkBizExists(id):
    id = id
    biz = Business.query.get(id)
    if biz:
        return biz
    else:
        return None



@reviewBlueprint.route('/api/businesses/<int:id>/reviews', methods=['GET'])
@swag_from('retrieveReviews.yml')
# @token_required
def getAllReviews(id):
    reviews = Review.query.filter_by(bizid=id)

    if reviews.count() != 0:
        return jsonify({'reviews':[review.returnJson() for review in reviews]}), 200
    else:
        return jsonify({'message':'No reviews Found for that business id'}), 404
