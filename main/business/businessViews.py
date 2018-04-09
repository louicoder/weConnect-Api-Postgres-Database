from flask import Blueprint, Flask, request, json, jsonify, make_response
import jwt
import datetime
from user.userViews import token_required, loggedInUser
from werkzeug.security import generate_password_hash, check_password_hash
from flasgger import swag_from
from appModels import Business, db
from flask_paginate import Pagination, get_page_args, get_page_parameter


businessBlueprint = Blueprint('business', __name__)

@businessBlueprint.route('/api/businesses', methods=['POST'])
@swag_from('createBusiness.yml')
# @token_required
def createBusiness():
    global loggedInUser
    jsn = request.data
    data = json.loads(jsn)

    #lets pick the data from json passed
    bizname = data['name']
    userid = loggedInUser['id']
    location =data['location']
    category = data['category']
    description = data['description']

    #lets create the business object with data from json but after we check that all fields are passed
    if not bizname or not userid or not location or not category or not description:
        return jsonify({'message':'some fields required are missing, please try again'}), 400
    else:
        if Business.query.filter_by(bizname=bizname).count() == 0:
            business = Business(userid, bizname, location, category, description)
            db.session.add(business)
            
            if business:
                return jsonify({'message':'business has been successfully created'}), 200
            else:
                return jsonify({'message':'business was not created, please try again'}), 400
        else:
            return jsonify({'message':'business already exists, please try again'})


@businessBlueprint.route('/api/businesses/<int:id>', methods=['GET'])
@swag_from('retrieveBusiness.yml')
# @token_required
def getOneBusiness(id):
    biz = Business.query.get(id)    
    if biz:
        return jsonify({'message':biz.returnJson()}), 200
    else:
        return jsonify({'message':'no business with id '+ str(id) +' exists'}), 404
    


@businessBlueprint.route('/api/businesses', methods=['GET'])
@swag_from('retrieveAllBusinesses.yml')
# @token_required
def getAllBusinesses():
    businesses = Business.query.all()
    if not businesses:
        return jsonify({'message':'No businesses exist, please register one'}), 404
    else:        
        return jsonify({'businesses':[business.returnJson() for business in businesses]}), 200
        


@businessBlueprint.route('/api/businesses/<int:id>', methods=['PUT'])
@swag_from('updateBusiness.yml')
# @token_required
def updatebusiness(id):
    global loggedInUser
    biz = Business.query.get(id)
    print(biz.id)

    if len(loggedInUser.keys()) != 3:
        return jsonify({'message':'You are not logged in.'})
    else:
        userid = loggedInUser['id']

    if biz.query.count() > 0:
        print(loggedInUser)
        
        jsn = request.data
        data = json.loads(jsn)

        if 'name' in data.keys():
            bizname = data['name']
        else:
            bizname = None

        if 'location' in data.keys():
            location =data['location']
        else:
            location = None

        if 'category' in data.keys():
            category = data['category']
        else:
            category = None

        if 'description' in data.keys():
            description = data['description']
        else:
            description = None        

        if biz.userid == str(userid):
            
            if bizname:
                biz.bizname = bizname
            if location:
                biz.location = location
            if category:
                biz.category = category
            if description:
                biz.description = description            
            print([bizname, location, category, description])
            db.session.add(biz)
        return jsonify({'message':'business '+ str(id) +' has been updated successfully'}), 200
        
    else:
        return jsonify({'message':'no business with id '+ str(id) +' exists'}), 404

        
@businessBlueprint.route('/api/businesses/<int:id>', methods=['DELETE'])
@swag_from('deleteBusiness.yml')
# @token_required
def deletebusiness(id):
    global loggedInUser
    userid = loggedInUser['id']
    biz = Business.query.get(id)
    print(userid == biz.id)
    if biz:
        if str(userid) == str(biz.id):
            db.session.delete(biz)
            return jsonify({'message':'business was deleted successfully'})
        else:
            return jsonify({'message':'business was not deleted because you are not the owner'})
    else:
        return jsonify({'message':'no business with that id exists'})


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

def getPaginatedResult(klass, url, start, limit):
    results = klass.query.all()
    count = len(results)

    if count < start:
        return jsonify({'message':'No records Found'}), 404

    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count

    if start == 1:
        obj['previous'] =''
    
    if start + limit > count:
        obj['next'] = ''

    obj['results']
    pass