from flask import Blueprint, Flask, request, json, jsonify, make_response, url_for, abort
import jwt
import datetime
from datetime import datetime
from ..user.userViews import token_required, logged_in_user
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from
from ..appModels import Business, db
from flask_paginate import Pagination, get_page_args, get_page_parameter


businessBlueprint = Blueprint('business', __name__)

@businessBlueprint.route('/api/businesses', methods=['POST'])
@swag_from('createBusiness.yml')
@token_required
def create_business():
    global logged_in_user
    jsn = request.data
    data = json.loads(jsn)

    specialChars = ['@', '#', '$', '%', '^', '&', '*', '!', '/', '?', '-', '_']

    if len(data.keys()) == 0:
        return jsonify({'message':'fill in all the fields that is name, location, category and description'}), 400 #bad request

    # if len(data.keys()) != 4:
    #     return jsonify({'message':'cannot create business because of missing fields'}), 400 #bad request
    
    if 'name' not in data.keys():
        return jsonify({'message':'business name is missing'}), 400 #bad request

    if 'location' not in data.keys():
        return jsonify({'message':'business location is missing'}), 400 #bad request

    if 'category' not in data.keys():
        return jsonify({'message':'business category is missing'}), 400 #bad request

    if 'description' not in data.keys():
        return jsonify({'message':'business description is missing'}), 400 #bad request

    if len(data['name']) < 5:
        return jsonify({'message':'name of business is too short, should between five and ten characters'}), 400 #bad request

    if len(data['name']) > 10:
        return jsonify({'message':'name of business is too long, should between five and ten characters'}), 400 #bad request

    if not logged_in_user:
        return jsonify({'message':'you are not logged in, please login'}), 400 #bad request

    if not logged_in_user:
        return jsonify({'message':'you are not logged in, please login'}), 400 #bad request

    #lets pick the data from json passed
    bizname = data['name']
    userid = logged_in_user['id']
    location =data['location']
    category = data['category']
    description = data['description']

    for x in bizname:
        if x in specialChars:
            return jsonify({'message':'business name contains special characters'}), 400

    
    if Business.query.filter_by(bizname=bizname).count() == 0:
        business = Business(userid, bizname, location, category, description)
        db.session.add(business)
        
        if business:
            return jsonify({'message':'business has been successfully created'}), 201
        else:
            return jsonify({'message':'business was not created, please try again'}), 400
    else:
        return jsonify({'message':'business already exists, please try again'}), 400

@businessBlueprint.route('/api/businesses/<int:id>', methods=['GET'])
@swag_from('retrieveBusiness.yml')
@token_required
def get_one_business(id):
    biz = Business.query.get(id)
    if biz:
        return jsonify({'businesses':biz.returnJson()}), 200
    else:
        return jsonify({'message':'no business with that id exists'}), 404

@businessBlueprint.route('/api/businesses', methods=['GET'])
@swag_from('retrieveAllBusinesses.yml')
@token_required
def get_all_businesses():
    businesses = Business.query.all()    
    if not businesses:
        return jsonify({'message':'no businesses exist, please register one'}), 404
    else:
        return jsonify({"businesses":[business.returnJson() for business in businesses]}), 200
        

@businessBlueprint.route('/api/businesses/<int:id>', methods=['PUT'])
@swag_from('updateBusiness.yml')
@token_required
def update_business(id):
    global logged_in_user
    jsn = request.data
    data = json.loads(jsn)
    biz = Business.query.get(int(id))    
    
    if not logged_in_user:
        return jsonify({"message":"please login"})

    if len(data.keys()) == 0:
        return jsonify({'message':'no information was provided for update'}), 400

    # if 'id' not in logged_in_user.keys():
    #     return jsonify({"message":"missing userid, cannot update business"})

    userid = logged_in_user['id']
    
    if biz.query.count() > 0 and userid == biz.userid:
        # print(logged_in_user)

        if 'name' in data.keys():
            bizname = data['name']
        else:
            bizname = ''

        if 'location' in data.keys():
            location =data['location']
        else:
            location = ''

        if 'category' in data.keys():
            category = data['category']
        else:
            category = ''

        if 'description' in data.keys():
            description = data['description']
        else:
            description = ''        
            
        if bizname:
            biz.bizname = bizname
        if location:
            biz.location = location
        if category:
            biz.category = category
        if description:
            biz.description = description   

        biz.date_modified = datetime.now()
        print([bizname, location, category, description])
        db.session.add(biz)
        db.session.commit()
        return jsonify({'message':'business has been updated successfully'}), 200
    else:
        return jsonify({'message':'no business with that id exists'}), 404

        
@businessBlueprint.route('/api/businesses/<int:id>', methods=['DELETE'])
@swag_from('deleteBusiness.yml')
# @token_required
def delete_business(id):
    global logged_in_user    
    biz = Business.query.get(int(id))

    if not logged_in_user:
        return jsonify({"message": "please login"}), 400

    userid = logged_in_user['id']
    
    if biz:
        if str(userid) == str(biz.id):
            db.session.delete(biz)
            db.session.commit()
            return jsonify({'message':'business was deleted successfully'})
        else:
            return jsonify({'message':'business was not deleted because you are not the owner'})
    else:
        return jsonify({'message':'no business with that id exists'})


@businessBlueprint.route('/api/businesses/search', methods=['GET'])
@swag_from('searchBusiness.yml')
# @token_required
def search_business():
    name = request.args.get('q')
    filter_type = str(request.args.get('filter_type'))
    filter_value = str(request.args.get('filter_value'))

    if not filter_type:
        return jsonify({'message':'filter type missing'}), 400

    if not filter_value:
        return jsonify({'message':'filter value missing'}), 400

    results = Business.query.filter_by(bizname=Business.bizname.ilike('%' + name + '%'))

    if filter_type == 'location':   
        results = Business.query.filter_by(bizname=name, location=filter_value).filter(Business.bizname.like("%"+ name +"%"))
    
    elif filter_type == 'category':
        results = Business.query.filter_by(bizname=name, category=filter_value).filter(Business.bizname.like("%"+ name +"%"))
    else:
        return jsonify({'message':'unknown filter type passed in query url'}), 400

    print(results)
    if results.count() > 0:
        print(results)
        return jsonify({'businesses':[res.returnJson() for res in results]}), 200
    else:
        return jsonify({'message':'no businesses match your search'}), 404


@businessBlueprint.route('/api/businesses/filter', methods=['GET'])
@swag_from('filterBusiness.yml')
# @token_required
def filter_business():
    filter_type = str(request.args.get('filter_type'))
    filter_value = str(request.args.get('filter_value'))

    if filter_type == 'location':
        results = Business.query.filter_by(location=filter_value)
    elif filter_type == 'category':
        results = Business.query.filter_by(category=filter_value)
    else:
        return jsonify({'message':'invalid or unknown filter type passed in query url'}), 400

    if not results:
        return jsonify({"message":"no businesses registered with that filter"}), 404

    return jsonify({"businesses":[business.returnJson() for business in results]}), 200