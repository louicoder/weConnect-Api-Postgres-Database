from flask import Blueprint, Flask, request, json, jsonify, make_response
from flasgger import swag_from
from ..user.userViews import token_required, logged_in_user
import sys
from flask_paginate import Pagination, get_page_args, get_page_parameter
from ..appModels import db, Business, Review

reviewBlueprint = Blueprint('reviews', __name__)
@reviewBlueprint.route('/api/businesses/<int:id>/reviews', methods=['POST'])
@swag_from('createReview.yml')
@token_required
def create_review(id):
    """Function is responsible fof creating a new review"""
    global logged_in_user
    jsn = request.data
    data = json.loads(jsn)
    id = id

    #check whether business exists before creating review
    exists = Review.check_business_exists(id)
    
    if exists:
        userid= exists.userid
        if 'review' in data.keys():
            review = data['review']
            rev = Review(review, int(userid), exists.id)
            db.session.add(rev)
            db.session.commit()
            return jsonify({'message':'review has been successfully created'}), 200
        else:
            return jsonify({'message':'missing field, review'}), 400
    else:
        return jsonify({'message':'no business with that id exists'}), 404


@reviewBlueprint.route('/api/businesses/<int:id>/reviews', methods=['GET'])
# @swag_from('retrieveReviews.yml')
@token_required
def get_all_reviews(id):
    
    if request.method == 'GET':
        limit = request.args.get('limit') or 2 # default is 5 in case limit is not set
        page = request.args.get('page') or 1
        limit = int(limit)
        page = int(page)

    reviews = Review.query.filter_by(business_id=id)

    results = reviews.paginate(per_page=limit, page=page, error_out=False)
    review_list = []
    for review in results.items:
        review_obj={
            'id':review.id,
            'review':review.review,
            'userid':review.userid,
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
        return jsonify({'message':'No reviews found for that business id'}), 404
