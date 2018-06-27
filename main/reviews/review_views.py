from flask import Blueprint, Flask, request, json, jsonify, make_response
from flasgger import swag_from
from ..user.user_views import token_required, logged_in_user
import sys
from flask_paginate import Pagination, get_page_args, get_page_parameter
from ..app_models import db, Business, Review
from flask_cors import CORS

reviewBlueprint = Blueprint('reviews', __name__)
CORS(reviewBlueprint)
@reviewBlueprint.route('/api/businesses/<int:business_id>/reviews', methods=['POST'])
# @swag_from('apidocs/create_review.yml')
@token_required
def create_review(business_id):
    """Function is responsible fof creating a new review"""
    global logged_in_user
    jsn = request.data
    data = json.loads(jsn)
    business_id = business_id

    businesses = Business.query.all()

    #check for atleast one existing business and if not throw Error "no business exists"
    if len(businesses) == 0:
        return jsonify({'message':'no businesses exist'}), 404

    #check whether business exists before creating review
    exists = Review.check_business_exists(int(business_id))
    
    if exists:
        user_id= exists.user_id
        if 'review' in data.keys():
            review = data['review']
            rev = Review(review, int(user_id), exists.id)
            db.session.add(rev)
            db.session.commit()
            return jsonify({'message':'review has been successfully created'}), 200
        else:
            return jsonify({'message':'review field missing'}), 400
    else:
        return jsonify({'message':'no business with that id exists'}), 400

# route 127.0.0.1:5000/api/businesses/<business_id>/reviews
@reviewBlueprint.route('/api/businesses/<int:business_id>/reviews', methods=['GET'])
# @swag_from('apidocs/retrieve_reviews.yml')
@token_required
def get_all_reviews(business_id):
    
    if request.method == 'GET':
        limit = request.args.get('limit') or 2 # default is 5 in case limit is not set
        page = request.args.get('page') or 1
        limit = int(limit)
        page = int(page)

    if type(business_id) != int:
        return jsonify({'message':'please enter a proper number for business id'}), 400

    # business = Business.query.filter_by(id=int(business_id))

    reviews = Review.query.filter_by(business_id=int(business_id))

    results = reviews.paginate(per_page=limit, page=page, error_out=False)
    review_list = []
    for review in results.items:
        review_obj={
            'id':review.id,
            'review':review.review,
            'user_id':review.user_id,
            'business_id':review.business_id,
            'date_created':review.date_created,
            'date_modified':review.date_modified,
            'per_page':results.per_page,
            'current_page':results.page,
            'total':results.total
        }
        review_list.append(review_obj)

    if len(review_list) > 0:
        return jsonify({'reviews':review_list}), 200
    else:
        return jsonify({'message':'no reviews found for that business id'}), 400
